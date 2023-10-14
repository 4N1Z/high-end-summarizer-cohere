import cohere
import streamlit as st
from nlpSummarizer import formattingForSummarizer
import PyPDF2
import re

co = cohere.Client(st.secrets["COHERE_API_KEY"]) 

# with open('content1.txt', 'r', encoding='utf-8') as file:
#     text = file.read()
st.header('SSW-Summarizer')
st.write('High End Summarizer Using Cohere Endpoints - Summarize any documents')


def split_text_into_sentences(text):
    # Split text into sentences using regular expressions
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
    return sentences

def summarzerMain(text) :
  responses = []
  text1 = text[:len(text)//2]
  text2 = text[len(text)//2:]

  summarizer_prompt  = "You should summarize the given content into meanigfull summaries.At the end give important keywords in JSON format  "

  # Add a header for the summary
  with st.sidebar:
      if st.button('Generate Summary'):
        print("___________ START __________")
        #when we click generate, i need to summarize text1 and text2 seperately
        with st.spinner('Generating response...'):
          for text in [text1, text2]:
            response = co.summarize( 
                  text=text,
                  length='long',
                  format='bullets',
                  model='summarize-xlarge',
                  additional_command= summarizer_prompt,
                  temperature=0.3,
            ) 
            print(response)
            responses.append(response.summary)
            #append the reponses list to a string
            
            print("PHASE 1 ONGOINGGGG")

          # Add a header for the summary
          st.markdown("<h3 style='color: green;'>Summary:</h3>", unsafe_allow_html=True)
          # After summarizing add these responses into co.chat and make it upto 300 words
          print("PHASE 1 Completed______________________")
          print("PHASE 2 ONGOING")

          chatResponses = ' '.join(responses)
          prompt_template = "Enlarge the given content into n number of paragraph response of `MORE THAN 500 WORDS` each. The content is : " + ' ' + chatResponses + "Give Response in a VERY EFFICIENT FORMAT, Preferabbly in BULLETS"
          response = co.generate(
                model='command',
                prompt= prompt_template,
                num_generations = 3,
                max_tokens= 400,
                temperature=0.3,
                k=0,
                stop_sequences=[],
                return_likelihoods='NONE'
            )
          
          
          # st.write(response)
          print("PHASE 2 Completed______________________")
          print('Prediction: {}'.format(response.generations[0].text))
          
          prediction_text = response.generations[0].text
          st.write(f'Prediction: {prediction_text}')
          st.write('Word Count:', len(prediction_text.split()))

          print("___________ END __________")
          # count words in summary
          # count = len(response.summary.split())
          # st.write('Word Count:', count)


def main ():
   
  uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf"]) 

  if 'read_more_clicked' not in st.session_state:
    st.session_state.read_more_clicked = False

  if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1]
    
    if file_extension.lower() == "pdf":
        # Read text from the PDF file
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        pdf_text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num] 
            pdf_text += page.extract_text()

        # Process the PDF text (you might need additional logic for PDF-specific formatting)
        st.markdown("<h4 style='color: #9D9D9D;'>Uploaded Content (PDF):</h4>", unsafe_allow_html=True)
        # Split text into sentences
        sentences = split_text_into_sentences(pdf_text)
        st.write('Word Count:', len(pdf_text.split()))

        # Display limited content with "Read More" functionality
        num_displayed_sentences = 2
        if len(sentences) > num_displayed_sentences:
            displayed_content = " ".join(sentences[:num_displayed_sentences])
            st.write(displayed_content)
            # if st.button("Read More"):
            #     st.write(" ".join(sentences))
            #     st.session_state.read_more_clicked = False
        else:
            st.write(pdf_text)
        processed_text = formattingForSummarizer(pdf_text)

    elif file_extension.lower() == "txt":
        # Read text from the TXT file
        text = uploaded_file.read().decode('utf-8')

        # Process the text
        st.markdown("<h4 style='color: #9D9D9D;'>Uploaded Content (PDF):</h4>", unsafe_allow_html=True)
        st.write('Word Count:', len(text.split()))
        # st.write(text)
        sentences = split_text_into_sentences(text)
        num_displayed_sentences = 2
        if len(sentences) > num_displayed_sentences:
            displayed_content = " ".join(sentences[:num_displayed_sentences])
            st.write(displayed_content)

        else:
            st.write(text)
        processed_text = formattingForSummarizer(text)
    else:
        st.write("Unsupported file format: As of now we only have the option to read a TXT or PDF file.")

    summarzerMain(processed_text)


if __name__ == "__main__" :
    main()
   
# Add the summary
