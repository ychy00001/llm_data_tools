import re

# Regex to strip repated copyright comment blocks
CPAT = re.compile("copyright", re.IGNORECASE)
PAT = re.compile("/\\*[^*]*\\*+(?:[^/*][^*]*\\*+)*/")


def clean_copyright_comments(content: str):
    r = PAT.search(content)
    if r:
        # found one, now see if it contains "copyright", if so strip it
        span = r.span()
        sub = content[span[0]:span[1]]
        if CPAT.search(sub):
            # cut it
            content = content[: span[0]] + content[span[1]:]

        return content

    lines = content.split('\n')
    skip = 0

    # Greedy replace any file that begins with comment block, most
    # are copyright headers
    for k in range(len(lines)):
        if (
                lines[k].startswith("//") or
                lines[k].startswith("#") or
                lines[k].startswith("--") or
                not lines[k]
        ):
            skip = skip + 1
        else:
            break

    if skip:
        # we skipped, consume it
        content = "\n".join(lines[skip:])

    return content


if __name__ == '__main__':
    total_text = ""
    with open("./test_copyright.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            total_text += line
    print(f"origin_text=====:\n {total_text}")
    format_txt = clean_copyright_comments(total_text)
    print(f"\n\n\nformat_text=====:\n {format_txt}")
