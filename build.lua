-- Directory containing generated HTML pages.
local pages_dir = "./pages"

-- Directory containing Markdown source files.
local markdown_dir = "./markdown"

-- Generated list of posts.
local post_list = "./post-list.html"

-- HTML templates.
local index_template = "./templates/index.template.html"
local post_template = "./templates/post.template.html"

-- Generated homepage.
local index_file = "./index.html"

-- Safely quote a path for use in a shell command.
local function shell_quote(value)
    return "'" .. value:gsub("'", "'\\''") .. "'"
end

-- Read and return the complete contents of a file.
local function read_file(path)
    local file = assert(io.open(path, "r"))
    local content = file:read("*a")
    file:close()
    return content
end

-- Write content to a file, replacing existing contents.
local function write_file(path, content)
    local file = assert(io.open(path, "w"))
    file:write(content)
    file:close()
end

-- Run a shell command and stop if it fails.
local function run(command)
    local ok = os.execute(command)

    if ok == nil or (type(ok) == "number" and ok ~= 0) then
        error("Command failed: " .. command)
    end
end

-- Escape special characters before inserting text into HTML.
local function html_escape(value)
    return value:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"):gsub('"', "&quot;"):gsub("'", "&#39;")
end

-- Find all Markdown files and store their paths.
local markdown_files = {}

local pipe = assert(io.popen("find " .. shell_quote(markdown_dir) .. " -type f -name '*.md' | sort"))

for file in pipe:lines() do
    table.insert(markdown_files, file)
end

pipe:close()

-- Sort posts according to their frontmatter order value.
table.sort(markdown_files, function(file_a, file_b)
    local content_a = read_file(file_a)
    local content_b = read_file(file_b)

    local frontmatter_a = content_a:match("^%-%-%-[\r\n]+(.-)[\r\n]+%-%-%-")
    local frontmatter_b = content_b:match("^%-%-%-[\r\n]+(.-)[\r\n]+%-%-%-")

    local order_a = frontmatter_a and tonumber(frontmatter_a:match("order:[ \t]*([^\r\n]+)")) or math.huge

    local order_b = frontmatter_b and tonumber(frontmatter_b:match("order:[ \t]*([^\r\n]+)")) or math.huge

    return order_a < order_b
end)

-- Create the output directory.
run("mkdir -p " .. shell_quote(pages_dir))

-- Remove previously generated files.
run("rm -f " .. shell_quote(pages_dir) .. "/*.html")
run("rm -f " .. shell_quote(post_list))
run("rm -f " .. shell_quote(index_file))

-- Store HTML links for the post list and homepage.
local posts = {}
local post_index = 0

-- Convert every Markdown file into an HTML page.
for _, markdown_file in ipairs(markdown_files) do
    -- Extract the filename without its directory or extension.
    local filename = markdown_file:match("([^/]+)%.md$")

    -- Read the Markdown source.
    local content = read_file(markdown_file)

    -- Use the frontmatter title, or the filename if no title exists.
    -- Extract the YAML frontmatter and read its title.
    local frontmatter = content:match("^%-%-%-[\r\n]+(.-)[\r\n]+%-%-%-")

    -- Read a single-line frontmatter value.
    local function frontmatter_value(name, fallback)
        if not frontmatter then
            return fallback
        end
        return frontmatter:match(name .. ":[ \t]*([^\r\n]+)") or fallback
    end

    local title = frontmatter_value("title", filename)
    local date = frontmatter_value("date", "")
    local details = frontmatter_value("details", "");

    -- Add the title and custom HTML to the index post list.
    table.insert(posts,
        string.format('<table><tr>' .. '<td class="post-title"><a href="pages/%s.html">%s</a></td></table>', filename,
            html_escape(title)))

    post_index = post_index + 1
    if post_index == 4 then
        table.insert(posts, "<br>")
    end

    -- table.insert(posts, string.format('<table><tr>' .. '<td class="post-title"><a href="pages/%s.html">%s</a></td>' ..
    --                                       '<td><span class="details_content">%s</span></td>' .. '</tr></table>',
    --     filename, html_escape(title), html_escape(details)))

    -- Set the output HTML path.
    local output_file = pages_dir .. "/" .. filename .. ".html"

    -- Use Pandoc to convert Markdown into a complete HTML page.
    run(string.format("pandoc %s --template %s -f markdown -t html --css /styles/style.css -s -o %s",
        shell_quote(markdown_file), shell_quote(post_template), shell_quote(output_file)))

    print(filename .. " done.")
end

-- Write the generated post links to post-list.html.
write_file(post_list, table.concat(posts, "\n") .. "\n")

-- Insert the generated post list into the index template.
local template = read_file(index_template)

local index_content = template:gsub("{{POST_LIST}}", function()
    return table.concat(posts, "\n")
end)

-- Write the completed homepage.
write_file(index_file, index_content)

print("Build complete.")
