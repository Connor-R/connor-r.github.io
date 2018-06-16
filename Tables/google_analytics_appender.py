import bs4
import os
import argparse

script = """
    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

    ga('create', 'UA-77536074-1', 'auto');
    ga('send', 'pageview');
"""


# method from https://stackoverflow.com/questions/35355225/edit-and-create-html-file-using-python
# and also from https://stackoverflow.com/questions/19123245/inserting-into-a-html-file-using-python
def add_google_analytics(file_path):


    with open(file_path) as in_file:
        txt = in_file.read()
        soup = bs4.BeautifulSoup(txt,"lxml")

        soup.append("\n")
        new_script = soup.new_tag("script")
        soup.append(new_script)

        last_script = soup.findAll("script")[-1]
        last_script.insert(0, script)



    with open(file_path, "w") as out_file:
        out_file.write(str(soup))
        

    file_name = file_path.split("/")[-1]
    print "\tadded Google Analytics script to " + str(file_name)


if __name__ == "__main__":     
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path',type=str,default="")

    args = parser.parse_args()
    
    add_google_analytics(args.file_path)

