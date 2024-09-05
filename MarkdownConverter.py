import os
import markdown

class html:

    def __init__(self, head):

        #os.mkdir(f"/Users/rohanraval/Desktop/Demo/")
        self.dir = f"/Users/rohanraval/Desktop/Demo/"
        self.head = head
        self.html_snippets = []

    def write(self, text):

        markdown_content = text
        html_body = markdown.markdown(markdown_content)


        html_content = f"""
        <div class="content-section">
            {html_body}
        </div>
        """


        self.html_snippets.append(html_content)

    def get_file(self):

        combined_html_content = "\n".join(self.html_snippets)


        combined_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Combined HTML</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 20px;
                    padding: 20px;
                    background-color: #f4f4f4;
                    color: #333;
                }}
                h3 {{
                    color: #0056b3;
                }}
                ul {{
                    list-style-type: disc;
                    margin-left: 20px;
                }}
                a {{
                    color: #0056b3;
                    text-decoration: none;
                }}
                .content-section {{
                    margin-bottom: 20px;
                }}
            </style>
        </head>
        <body>
            {combined_html_content}
        </body>
        </html>
        """

        with open(self.dir + f"{self.head}.html", 'w') as combined_file:
            combined_file.write(combined_html)
