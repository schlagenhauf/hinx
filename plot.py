#%%
# Dev Steps
# 1. Bring hiplot up. Works, generates HTML
# 2. Try out how capture groups work in python: https://docs.python.org/3/library/re.html#re.Match.group
# 3. Parse a line in a predefined format
# 4. Generate regex pattern from log_format
# 5. Read data from dump
# 6. Throw data in hiplot

#%%
import re
import hiplot as hip

log_format = '$host $remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"'

with open('access.log', 'r') as f:
    data = f.read()

lines = data.splitlines()

def parse_log(lines, log_format):
    log_format = re.escape(log_format)
    field_matcher = re.compile(r'\\\$([A-Za-z_]+)')  # match field names
    field_names = field_matcher.findall(log_format)
    regex_log_format = f"^{field_matcher.sub(r'(.+?)', log_format)}$"

    line_matcher = re.compile(regex_log_format)

    data = []

    for line in lines:
        line_match = line_matcher.match(line)
        if line_match:
            data.append(dict(zip(field_names, line_match.groups())))

    return data


data = parse_log(lines, log_format)

blacklist = ['request', 'http_user_agent', 'time_local']
data = [{k:v for k, v in d.items() if k not in blacklist} for d in data]

exp = hip.Experiment.from_iterable(data)
exp.display_data(hip.Displays.PARALLEL_PLOT)['categoricalMaximumValues'] = 1e6
exp.to_html("index.html")
#exp.display()

