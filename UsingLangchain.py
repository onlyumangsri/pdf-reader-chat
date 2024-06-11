# import os
# from langchain.chains import RetrievalQA
# from langchain_community.llms import OpenAI  # Updated import
# from langchain_community.document_loaders import PyPDFLoader  # Updated import
# from langchain.text_splitter import CharacterTextSplitter
# from langchain_community.embeddings import OpenAIEmbeddings  # Updated import
# from langchain_community.vectorstores import Chroma  # Updated import
# import panel as pn

import os
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI  # Updated import
from langchain_community.document_loaders import PyPDFLoader  # Updated import
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings  # Updated import
from langchain_community.vectorstores import Chroma  # Updated import
import panel as pn

file_input = pn.widgets.FileInput(width=300)

openaikey = pn.widgets.PasswordInput(
    value="", placeholder="Enter your OpenAI API Key here...", width=300
)
prompt = pn.widgets.TextEditor(
    value="", placeholder="Enter your questions here...", height=160, toolbar=False
)
run_button = pn.widgets.Button(name="Run!")

select_k = pn.widgets.IntSlider(
    name="Number of relevant chunks", start=1, end=5, step=1, value=2
)
select_chain_type = pn.widgets.RadioButtonGroup(
    name='Chain type',
    options=['stuff', 'map_reduce', "refine", "map_rerank"]
)

widgets = pn.Row(
    pn.Column(prompt, run_button, margin=5),
    pn.Card(
        "Chain type:",
        pn.Column(select_chain_type, select_k),
        title="Advanced settings", margin=10
    ), width=600
)

def qa(file, query, chain_type, k):
    loader = PyPDFLoader(file)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(texts, embeddings)
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k})
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(), chain_type=chain_type, retriever=retriever, return_source_documents=True)
    result = qa({"query": query})
    print(result['result'])
    return result

convos = [] 

def qa_result(_):
    os.environ["OPENAI_API_KEY"] = openaikey.value
    temp_dir = "/tmp/cache"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, "temp.pdf")

    # save pdf file to a temp file
    if file_input.value is not None:
        file_input.save(temp_file_path)

        prompt_text = prompt.value
        if prompt_text:
            result = qa(file=temp_file_path, query=prompt_text, chain_type=select_chain_type.value, k=select_k.value)
            convos.extend([
                pn.Row(
                    pn.panel("\U0001F60A", width=10),
                    prompt_text,
                    width=600
                ),
                pn.Row(
                    pn.panel("\U0001F916", width=10),
                    pn.Column(
                        result["result"],
                        "Relevant source text:",
                        pn.pane.Markdown('\n--------------------------------------------------------------------\n'.join(doc.page_content for doc in result["source_documents"]))
                    )
                )
            ])
            #return convos
    return pn.Column(*convos, margin=15, width=575, min_height=400)

qa_interactive = pn.panel(
    pn.bind(qa_result, run_button),
    loading_indicator=True,
)

output = pn.WidgetBox('*Output will show up here:*', qa_interactive, width=630, scroll=True)

pn.Column(
    pn.pane.Markdown("""
    ## \U0001F60A! Question Answering with your PDF file

    Step 1: Upload a PDF file \n
    Step 2: Enter your OpenAI API key. This costs $$. You will need to set up billing info at [OpenAI](https://platform.openai.com/account). \n
    Step 3: Type your question at the bottom and click "Run" \n

    """),
    pn.Row(file_input, openaikey),
    output,
    widgets

).servable()
