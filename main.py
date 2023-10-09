import cohere
import streamlit as st
from nlpSummarizer import formattingForSummarizer
co = cohere.Client(st.secrets["COHERE_API_KEY"]) 

# with open('content1.txt', 'r', encoding='utf-8') as file:
#     text = file.read()

st.title('High End Summarizer Using Cohere Endpoints')


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
              format='paragraph',
              model='summarize-xlarge',
              additional_command= summarizer_prompt,
              temperature=0.3,
            ) 
            print(response)
            responses.append(response.summary)
            #append the reponses list to a string
            
            print("PHASE 1 ONGOINGGGG")

          # Add a header for the summary
          st.markdown("<h2 style='color: green;'>Summary:</h2>", unsafe_allow_html=True)
          # After summarizing add these responses into co.chat and make it upto 300 words
          print("PHASE 1 Completed______________________")
          print("PHASE 2 ONGOING")

          chatResponses = ' '.join(responses)
          prompt_template = "Enlarge the given content into 5 paragraph response of `MORE THAN 500 WORDS` each. The content is : " + ' ' + chatResponses
          response = co.generate(
            model='command-nightly',
            prompt= prompt_template,
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
   
  uploaded_file = st.file_uploader("Upload a file", type=["txt"]) 
  if uploaded_file is not None:

    text = uploaded_file.read().decode('utf-8')
    st.markdown("<h2 style='color: red;'>Uploaded Content:</h2>", unsafe_allow_html=True)
    st.write('Word Count:', len(text.split()))
    st.write(text)
    text = formattingForSummarizer(text)

    # Add a header for the original text
    # st.markdown("<h2 style='color: blue;'>Original Text:</h2>", unsafe_allow_html=True)
    # st.write(text)
    # split the text into 2 equal halves

    
    summarzerMain(text)


if __name__ == "__main__" :
    main()
   
# Add the summary
