
def formattingForSummarizer(text):
    for each in text :
        if (each == "'") :
            text = text.replace(each, "")
        if(each == "`"):
            text = text.replace(each, "")    
    
        # print("____EACH____", each, "\n")

    # remove spaces and newlines
    text = text.replace('\n', ' ').replace('\r', '').replace('\t', ' ')
    # ("____TEXT____", text, "\n")
    return text
 
# def main ():

#     # demoCohere()

#     # with open('content.txt', 'r', encoding='utf-8') as file:
#     #     text = file.read()
#     # formattingForSummarizer(text)


# if __name__ == "__main__" :
#     main()