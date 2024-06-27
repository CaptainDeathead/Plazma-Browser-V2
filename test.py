from bs4 import BeautifulSoup
from bs4.element import NavigableString

html = """
<html>
    <head>
        <title>E</title>
    </head>

    <body>
        <p>
            Just p
            <b>bold</b>
        </p>
    </body>
</html>
"""

soup = BeautifulSoup(html, 'html.parser')

nodeStack = [soup]

while len(nodeStack) > 0:
    node = nodeStack.pop()

    print(node.name)

    for child in reversed(list(node.children)):
        if isinstance(child, NavigableString):
            print(child.text.replace('\n', ''))
            continue

        nodeStack.append(child)