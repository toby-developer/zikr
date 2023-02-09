try:
    badContent = bsObj.nonExistingTag.anotherTag
except AttributeError as e:
    if badContent == None:
        print("Tag could not be found")
    else:
        print(badContent)