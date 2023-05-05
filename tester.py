import sfactory
import classroom
import datetime
import tiktoken

#
enc = tiktoken.get_encoding("cl100k_base")
assert enc.decode(enc.encode("hello world")) == "hello world"
enc = tiktoken.encoding_for_model("gpt-3.5-turbo")

print(enc)

#sfactory.createS()
#print(sfactory.chatGPT("What is the weather in Northern Cape?"))
"""cw = classroom.getCourseLoadByID(598260968944)

#print(cw)
for x in cw["courseWork"]:
    print(x["title"])
    try:
        print()
    except:
        print("No due date")
#print(classroom.getAllClasses())
#print(sfactory.createS())"""