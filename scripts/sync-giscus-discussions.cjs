const { execFileSync } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

const DEFAULT_REPOSITORY = "didilili/ai-agents-from-zero";
const START_MARKER = "  // giscus-discussions:start";
const END_MARKER = "  // giscus-discussions:end";
const ROUTES_START_MARKER = "  // giscus-routes:start";
const ROUTES_END_MARKER = "  // giscus-routes:end";

const DISCUSSIONS_QUERY = `
  query($owner: String!, $name: String!, $after: String) {
    repository(owner: $owner, name: $name) {
      discussions(first: 100, after: $after) {
        nodes {
          number
          title
          createdAt
          comments {
            totalCount
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  }
`;

function commentCount(discussion) {
  return Number(discussion.comments?.totalCount || 0);
}

function selectDiscussionNumbers(discussions) {
  const groups = new Map();

  for (const discussion of discussions) {
    const title = String(discussion.title || "").trim();
    if (!title) continue;

    const group = groups.get(title) || [];
    group.push(discussion);
    groups.set(title, group);
  }

  const selected = [];
  const duplicates = [];

  for (const [title, group] of groups) {
    group.sort(
      (left, right) =>
        commentCount(right) - commentCount(left) ||
        new Date(left.createdAt).getTime() -
          new Date(right.createdAt).getTime() ||
        left.number - right.number,
    );

    const canonical = group[0];
    selected.push({ title, number: canonical.number });

    if (group.length > 1) {
      duplicates.push({
        title,
        selected: canonical.number,
        skipped: group.slice(1).map((discussion) => discussion.number),
      });
    }
  }

  selected.sort((left, right) => left.number - right.number);
  duplicates.sort((left, right) => left.selected - right.selected);

  return {
    discussionNumbers: Object.fromEntries(
      selected.map(({ title, number }) => [title, number]),
    ),
    duplicates,
  };
}

function replaceGeneratedMap(
  source,
  startMarker,
  endMarker,
  variableName,
  map,
) {
  const start = source.indexOf(startMarker);
  const end = source.indexOf(endMarker);

  if (start === -1 || end === -1 || end <= start) {
    throw new Error(`Could not find the generated ${variableName} map markers`);
  }

  const serialized = JSON.stringify(map, null, 2)
    .split("\n")
    .map((line, index) => (index === 0 ? line : `  ${line}`))
    .join("\n");
  const generated = `${startMarker}\n  var ${variableName} = ${serialized};\n${endMarker}`;

  return (
    source.slice(0, start) + generated + source.slice(end + endMarker.length)
  );
}

function replaceDiscussionNumbers(source, discussionNumbers) {
  return replaceGeneratedMap(
    source,
    START_MARKER,
    END_MARKER,
    "discussionNumbers",
    discussionNumbers,
  );
}

function replaceDiscussionRoutes(source, discussionRoutes) {
  return replaceGeneratedMap(
    source,
    ROUTES_START_MARKER,
    ROUTES_END_MARKER,
    "discussionRoutes",
    discussionRoutes,
  );
}

function normalizeSidebarRoute(href) {
  let route = String(href || "").trim();
  if (!route || /^(?:https?:|mailto:|#)/i.test(route)) return null;

  route = route.split("?")[0].split("#")[0].replace(/^\/+/, "");
  try {
    route = decodeURIComponent(route);
  } catch (_error) {
    // Keep the original route when it contains malformed escape sequences.
  }

  route = route.replace(/^translations\/en\/?/, "");
  if (!route || route.endsWith("/")) route += "README.md";

  return route;
}

function parseSidebarLinks(source) {
  const links = [];
  const pattern = /\[([^\]]+)\]\(([^)]+)\)/g;
  let match;

  while ((match = pattern.exec(source))) {
    const route = normalizeSidebarRoute(match[2]);
    if (route) links.push({ title: match[1].trim(), route });
  }

  return links;
}

function buildDiscussionRoutes(
  chineseSidebar,
  englishSidebar,
  discussionNumbers,
  overrides = {},
) {
  const englishTitles = new Map(
    parseSidebarLinks(englishSidebar).map(({ route, title }) => [route, title]),
  );
  const routeNumbers = new Map();

  for (const { route, title } of parseSidebarLinks(chineseSidebar)) {
    const englishTitle = englishTitles.get(route);
    const number =
      discussionNumbers[title] ||
      (englishTitle ? discussionNumbers[englishTitle] : undefined);
    if (number) routeNumbers.set(route, number);
  }

  for (const [route, number] of Object.entries(overrides)) {
    routeNumbers.set(route, number);
  }

  return Object.fromEntries(
    [...routeNumbers]
      .sort(
        ([leftRoute, leftNumber], [rightRoute, rightNumber]) =>
          leftNumber - rightNumber || leftRoute.localeCompare(rightRoute),
      )
      .map(([route, number]) => [route, number]),
  );
}

function fetchDiscussions(repository = DEFAULT_REPOSITORY) {
  const [owner, name, extra] = repository.split("/");
  if (!owner || !name || extra) {
    throw new Error(`Invalid GitHub repository: ${repository}`);
  }

  const discussions = [];
  let cursor;

  do {
    const args = [
      "api",
      "graphql",
      "-f",
      `query=${DISCUSSIONS_QUERY}`,
      "-f",
      `owner=${owner}`,
      "-f",
      `name=${name}`,
    ];
    if (cursor) args.push("-f", `after=${cursor}`);

    let response;
    try {
      response = JSON.parse(
        execFileSync("gh", args, {
          encoding: "utf8",
          stdio: ["ignore", "pipe", "pipe"],
        }),
      );
    } catch (error) {
      const detail = error.stderr?.toString().trim() || error.message;
      throw new Error(`Could not read GitHub Discussions with gh: ${detail}`);
    }

    const connection = response.data?.repository?.discussions;
    if (!connection) {
      throw new Error(`GitHub returned no Discussions data for ${repository}`);
    }

    discussions.push(...connection.nodes);
    cursor = connection.pageInfo.hasNextPage
      ? connection.pageInfo.endCursor
      : undefined;
  } while (cursor);

  return discussions;
}

function syncDiscussionNumbers() {
  const root = path.resolve(__dirname, "..");
  const pluginPath = path.join(root, "lib/plugins/giscus.js");
  const repository = process.env.GISCUS_REPO || DEFAULT_REPOSITORY;
  const discussions = fetchDiscussions(repository);
  const selection = selectDiscussionNumbers(discussions);
  const discussionRoutes = buildDiscussionRoutes(
    fs.readFileSync(path.join(root, "_sidebar.md"), "utf8"),
    fs.readFileSync(path.join(root, "_sidebar.en.md"), "utf8"),
    selection.discussionNumbers,
    { "README.md": 5 },
  );
  const source = fs.readFileSync(pluginPath, "utf8");
  const updated = replaceDiscussionRoutes(
    replaceDiscussionNumbers(source, selection.discussionNumbers),
    discussionRoutes,
  );

  if (updated !== source) {
    fs.writeFileSync(pluginPath, updated);
  }

  console.log(
    `Synced ${Object.keys(selection.discussionNumbers).length} discussion titles and ${Object.keys(discussionRoutes).length} shared routes from ${repository}.`,
  );

  for (const duplicate of selection.duplicates) {
    console.warn(
      `Duplicate title: ${duplicate.title}; selected #${duplicate.selected}, skipped ${duplicate.skipped.map((number) => `#${number}`).join(", ")}.`,
    );
  }
}

module.exports = {
  buildDiscussionRoutes,
  fetchDiscussions,
  normalizeSidebarRoute,
  replaceDiscussionNumbers,
  replaceDiscussionRoutes,
  selectDiscussionNumbers,
  syncDiscussionNumbers,
};

if (require.main === module) {
  try {
    syncDiscussionNumbers();
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}
