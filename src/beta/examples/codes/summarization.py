# Summarization
# A summarization chain can be used to summarize multiple documents. One way is to input multiple smaller documents, after they have been divided into chunks, and operate over them with a MapReduceDocumentsChain. You can also choose instead for the chain that does summarization to be a StuffDocumentsChain, or a RefineDocumentsChain.

# Prepare Data
# First we prepare the data. For this example we create multiple documents from one long one, but these documents could be fetched in any manner (the point of this notebook to highlight what to do AFTER you fetch the documents).

from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.chains.mapreduce import MapReduceChain
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter

llm = OpenAI(temperature=0)

text_splitter = CharacterTextSplitter()

with open("../../state_of_the_union.txt") as f:
    state_of_the_union = f.read()
texts = text_splitter.split_text(state_of_the_union)

docs = [Document(page_content=t) for t in texts[:3]]

# Quickstart
# If you just want to get started as quickly as possible, this is the recommended way to do it:

from langchain.chains.summarize import load_summarize_chain

chain = load_summarize_chain(llm, chain_type="map_reduce")
chain.run(docs)

# ' In response to Russian aggression in Ukraine, the United States and its allies are taking action to hold Putin accountable, including economic sanctions, asset seizures, and military assistance. The US is also providing economic and humanitarian aid to Ukraine, and has passed the American Rescue Plan and the Bipartisan Infrastructure Law to help struggling families and create jobs. The US remains unified and determined to protect Ukraine and the free world.'

# If you want more control and understanding over what is happening, please see the information below.

# The stuff Chain
# This sections shows results of using the stuff Chain to do summarization.

chain = load_summarize_chain(llm, chain_type="stuff")

chain.run(docs)

# ' In his speech, President Biden addressed the crisis in Ukraine, the American Rescue Plan, and the Bipartisan Infrastructure Law. He discussed the need to invest in America, educate Americans, and build the economy from the bottom up. He also announced the release of 60 million barrels of oil from reserves around the world, and the creation of a dedicated task force to go after the crimes of Russian oligarchs. He concluded by emphasizing the need to Buy American and use taxpayer dollars to rebuild America.'

# Custom Prompts

# You can also use your own prompts with this chain. In this example, we will respond in Italian.

prompt_template = """Write a concise summary of the following:


{text}


CONCISE SUMMARY IN ITALIAN:"""
PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
chain = load_summarize_chain(llm, chain_type="stuff", prompt=PROMPT)
chain.run(docs)

# "\n\nIn questa serata, il Presidente degli Stati Uniti ha annunciato una serie di misure per affrontare la crisi in Ucraina, causata dall'aggressione di Putin. Ha anche annunciato l'invio di aiuti economici, militari e umanitari all'Ucraina. Ha anche annunciato che gli Stati Uniti e i loro alleati stanno imponendo sanzioni economiche a Putin e stanno rilasciando 60 milioni di barili di petrolio dalle riserve di tutto il mondo. Inoltre, ha annunciato che il Dipartimento di Giustizia degli Stati Uniti sta creando una task force dedicata ai crimini degli oligarchi russi. Il Presidente ha anche annunciato l'approvazione della legge bipartitica sull'infrastruttura, che prevede investimenti per la ricostruzione dell'America. Questo porterà a creare posti"

# The map_reduce Chain
# This sections shows results of using the map_reduce Chain to do summarization.

chain = load_summarize_chain(llm, chain_type="map_reduce")

chain.run(docs)

# " In response to Russia's aggression in Ukraine, the United States and its allies have imposed economic sanctions and are taking other measures to hold Putin accountable. The US is also providing economic and military assistance to Ukraine, protecting NATO countries, and releasing oil from its Strategic Petroleum Reserve. President Biden and Vice President Harris have passed legislation to help struggling families and rebuild America's infrastructure."

# Intermediate Steps

# We can also return the intermediate steps for map_reduce chains, should we want to inspect them. This is done with the return_map_steps variable.

chain = load_summarize_chain(
    OpenAI(temperature=0), chain_type="map_reduce", return_intermediate_steps=True
)

chain({"input_documents": docs}, return_only_outputs=True)

# {'map_steps': [" In response to Russia's aggression in Ukraine, the United States has united with other freedom-loving nations to impose economic sanctions and hold Putin accountable. The U.S. Department of Justice is also assembling a task force to go after the crimes of Russian oligarchs and seize their ill-gotten gains.",
#   ' The United States and its European allies are taking action to punish Russia for its invasion of Ukraine, including seizing assets, closing off airspace, and providing economic and military assistance to Ukraine. The US is also mobilizing forces to protect NATO countries and has released 30 million barrels of oil from its Strategic Petroleum Reserve to help blunt gas prices. The world is uniting in support of Ukraine and democracy, and the US stands with its Ukrainian-American citizens.',
#   " President Biden and Vice President Harris ran for office with a new economic vision for America, and have since passed the American Rescue Plan and the Bipartisan Infrastructure Law to help struggling families and rebuild America's infrastructure. This includes creating jobs, modernizing roads, airports, ports, and waterways, replacing lead pipes, providing affordable high-speed internet, and investing in American products to support American jobs."],
#  'output_text': " In response to Russia's aggression in Ukraine, the United States and its allies have imposed economic sanctions and are taking other measures to hold Putin accountable. The US is also providing economic and military assistance to Ukraine, protecting NATO countries, and passing legislation to help struggling families and rebuild America's infrastructure. The world is uniting in support of Ukraine and democracy, and the US stands with its Ukrainian-American citizens."}

# Custom Prompts

# You can also use your own prompts with this chain. In this example, we will respond in Italian.

prompt_template = """Write a concise summary of the following:


{text}


CONCISE SUMMARY IN ITALIAN:"""
PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
chain = load_summarize_chain(
    OpenAI(temperature=0),
    chain_type="map_reduce",
    return_intermediate_steps=True,
    map_prompt=PROMPT,
    combine_prompt=PROMPT,
)
chain({"input_documents": docs}, return_only_outputs=True)

# {'intermediate_steps': ["\n\nQuesta sera, ci incontriamo come democratici, repubblicani e indipendenti, ma soprattutto come americani. La Russia di Putin ha cercato di scuotere le fondamenta del mondo libero, ma ha sottovalutato la forza della gente ucraina. Gli Stati Uniti e i loro alleati stanno ora imponendo sanzioni economiche a Putin e stanno tagliando l'accesso della Russia alla tecnologia. Il Dipartimento di Giustizia degli Stati Uniti sta anche creando una task force dedicata per andare dopo i crimini degli oligarchi russi.",
#   "\n\nStiamo unendo le nostre forze con quelle dei nostri alleati europei per sequestrare yacht, appartamenti di lusso e jet privati di Putin. Abbiamo chiuso lo spazio aereo americano ai voli russi e stiamo fornendo più di un miliardo di dollari in assistenza all'Ucraina. Abbiamo anche mobilitato le nostre forze terrestri, aeree e navali per proteggere i paesi della NATO. Abbiamo anche rilasciato 60 milioni di barili di petrolio dalle riserve di tutto il mondo, di cui 30 milioni dalla nostra riserva strategica di petrolio. Stiamo affrontando una prova reale e ci vorrà del tempo, ma alla fine Putin non riuscirà a spegnere l'amore dei popoli per la libertà.",
#   "\n\nIl Presidente Biden ha lottato per passare l'American Rescue Plan per aiutare le persone che soffrivano a causa della pandemia. Il piano ha fornito sollievo economico immediato a milioni di americani, ha aiutato a mettere cibo sulla loro tavola, a mantenere un tetto sopra le loro teste e a ridurre il costo dell'assicurazione sanitaria. Il piano ha anche creato più di 6,5 milioni di nuovi posti di lavoro, il più alto numero di posti di lavoro creati in un anno nella storia degli Stati Uniti. Il Presidente Biden ha anche firmato la legge bipartitica sull'infrastruttura, la più ampia iniziativa di ricostruzione della storia degli Stati Uniti. Il piano prevede di modernizzare le strade, gli aeroporti, i porti e le vie navigabili in"],
#  'output_text': "\n\nIl Presidente Biden sta lavorando per aiutare le persone che soffrono a causa della pandemia attraverso l'American Rescue Plan e la legge bipartitica sull'infrastruttura. Gli Stati Uniti e i loro alleati stanno anche imponendo sanzioni economiche a Putin e tagliando l'accesso della Russia alla tecnologia. Stanno anche sequestrando yacht, appartamenti di lusso e jet privati di Putin e fornendo più di un miliardo di dollari in assistenza all'Ucraina. Alla fine, Putin non riuscirà a spegnere l'amore dei popoli per la libertà."}

# The refine Chain
# This sections shows results of using the refine Chain to do summarization.

chain = load_summarize_chain(llm, chain_type="refine")

chain.run(docs)

# "\n\nIn response to Russia's aggression in Ukraine, the United States has united with other freedom-loving nations to impose economic sanctions and hold Putin accountable. The U.S. Department of Justice is also assembling a task force to go after the crimes of Russian oligarchs and seize their ill-gotten gains. We are joining with our European allies to find and seize the assets of Russian oligarchs, including yachts, luxury apartments, and private jets. The U.S. is also closing off American airspace to all Russian flights, further isolating Russia and adding an additional squeeze on their economy. The U.S. and its allies are providing support to the Ukrainians in their fight for freedom, including military, economic, and humanitarian assistance. The U.S. is also mobilizing ground forces, air squadrons, and ship deployments to protect NATO countries. The U.S. and its allies are also releasing 60 million barrels of oil from reserves around the world, with the U.S. contributing 30 million barrels from its own Strategic Petroleum Reserve. In addition, the U.S. has passed the American Rescue Plan to provide immediate economic relief for tens of millions of Americans, and the Bipartisan Infrastructure Law to rebuild America and create jobs. This investment will"

# Intermediate Steps

# We can also return the intermediate steps for refine chains, should we want to inspect them. This is done with the return_refine_steps variable.

chain = load_summarize_chain(
    OpenAI(temperature=0), chain_type="refine", return_intermediate_steps=True
)

chain({"input_documents": docs}, return_only_outputs=True)

# {'refine_steps': [" In response to Russia's aggression in Ukraine, the United States has united with other freedom-loving nations to impose economic sanctions and hold Putin accountable. The U.S. Department of Justice is also assembling a task force to go after the crimes of Russian oligarchs and seize their ill-gotten gains.",
#   "\n\nIn response to Russia's aggression in Ukraine, the United States has united with other freedom-loving nations to impose economic sanctions and hold Putin accountable. The U.S. Department of Justice is also assembling a task force to go after the crimes of Russian oligarchs and seize their ill-gotten gains. We are joining with our European allies to find and seize the assets of Russian oligarchs, including yachts, luxury apartments, and private jets. The U.S. is also closing off American airspace to all Russian flights, further isolating Russia and adding an additional squeeze on their economy. The U.S. and its allies are providing support to the Ukrainians in their fight for freedom, including military, economic, and humanitarian assistance. The U.S. is also mobilizing ground forces, air squadrons, and ship deployments to protect NATO countries. The U.S. and its allies are also releasing 60 million barrels of oil from reserves around the world, with the U.S. contributing 30 million barrels from its own Strategic Petroleum Reserve. Putin's war on Ukraine has left Russia weaker and the rest of the world stronger, with the world uniting in support of democracy and peace.",
#   "\n\nIn response to Russia's aggression in Ukraine, the United States has united with other freedom-loving nations to impose economic sanctions and hold Putin accountable. The U.S. Department of Justice is also assembling a task force to go after the crimes of Russian oligarchs and seize their ill-gotten gains. We are joining with our European allies to find and seize the assets of Russian oligarchs, including yachts, luxury apartments, and private jets. The U.S. is also closing off American airspace to all Russian flights, further isolating Russia and adding an additional squeeze on their economy. The U.S. and its allies are providing support to the Ukrainians in their fight for freedom, including military, economic, and humanitarian assistance. The U.S. is also mobilizing ground forces, air squadrons, and ship deployments to protect NATO countries. The U.S. and its allies are also releasing 60 million barrels of oil from reserves around the world, with the U.S. contributing 30 million barrels from its own Strategic Petroleum Reserve. In addition, the U.S. has passed the American Rescue Plan to provide immediate economic relief for tens of millions of Americans, and the Bipartisan Infrastructure Law to rebuild America and create jobs. This includes investing"],
#  'output_text': "\n\nIn response to Russia's aggression in Ukraine, the United States has united with other freedom-loving nations to impose economic sanctions and hold Putin accountable. The U.S. Department of Justice is also assembling a task force to go after the crimes of Russian oligarchs and seize their ill-gotten gains. We are joining with our European allies to find and seize the assets of Russian oligarchs, including yachts, luxury apartments, and private jets. The U.S. is also closing off American airspace to all Russian flights, further isolating Russia and adding an additional squeeze on their economy. The U.S. and its allies are providing support to the Ukrainians in their fight for freedom, including military, economic, and humanitarian assistance. The U.S. is also mobilizing ground forces, air squadrons, and ship deployments to protect NATO countries. The U.S. and its allies are also releasing 60 million barrels of oil from reserves around the world, with the U.S. contributing 30 million barrels from its own Strategic Petroleum Reserve. In addition, the U.S. has passed the American Rescue Plan to provide immediate economic relief for tens of millions of Americans, and the Bipartisan Infrastructure Law to rebuild America and create jobs. This includes investing"}

# Custom Prompts

# You can also use your own prompts with this chain. In this example, we will respond in Italian.

prompt_template = """Write a concise summary of the following:


{text}


CONCISE SUMMARY IN ITALIAN:"""
PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
refine_template = (
    "Your job is to produce a final summary\n"
    "We have provided an existing summary up to a certain point: {existing_answer}\n"
    "We have the opportunity to refine the existing summary"
    "(only if needed) with some more context below.\n"
    "------------\n"
    "{text}\n"
    "------------\n"
    "Given the new context, refine the original summary in Italian"
    "If the context isn't useful, return the original summary."
)
refine_prompt = PromptTemplate(
    input_variables=["existing_answer", "text"],
    template=refine_template,
)
chain = load_summarize_chain(
    OpenAI(temperature=0),
    chain_type="refine",
    return_intermediate_steps=True,
    question_prompt=PROMPT,
    refine_prompt=refine_prompt,
)
chain({"input_documents": docs}, return_only_outputs=True)

# {'intermediate_steps': ["\n\nQuesta sera, ci incontriamo come democratici, repubblicani e indipendenti, ma soprattutto come americani. La Russia di Putin ha cercato di scuotere le fondamenta del mondo libero, ma ha sottovalutato la forza della gente ucraina. Insieme ai nostri alleati, stiamo imponendo sanzioni economiche, tagliando l'accesso della Russia alla tecnologia e bloccando i suoi più grandi istituti bancari dal sistema finanziario internazionale. Il Dipartimento di Giustizia degli Stati Uniti sta anche assemblando una task force dedicata per andare dopo i crimini degli oligarchi russi.",
#  "\n\nQuesta sera, ci incontriamo come democratici, repubblicani e indipendenti, ma soprattutto come americani. La Russia di Putin ha cercato di scuotere le fondamenta del mondo libero, ma ha sottovalutato la forza della gente ucraina. Insieme ai nostri alleati, stiamo imponendo sanzioni economiche, tagliando l'accesso della Russia alla tecnologia, bloccando i suoi più grandi istituti bancari dal sistema finanziario internazionale e chiudendo lo spazio aereo americano a tutti i voli russi. Il Dipartimento di Giustizia degli Stati Uniti sta anche assemblando una task force dedicata per andare dopo i crimini degli oligarchi russi. Stiamo fornendo più di un miliardo di dollari in assistenza diretta all'Ucraina e fornendo assistenza militare,",
#  "\n\nQuesta sera, ci incontriamo come democratici, repubblicani e indipendenti, ma soprattutto come americani. La Russia di Putin ha cercato di scuotere le fondamenta del mondo libero, ma ha sottovalutato la forza della gente ucraina. Insieme ai nostri alleati, stiamo imponendo sanzioni economiche, tagliando l'accesso della Russia alla tecnologia, bloccando i suoi più grandi istituti bancari dal sistema finanziario internazionale e chiudendo lo spazio aereo americano a tutti i voli russi. Il Dipartimento di Giustizia degli Stati Uniti sta anche assemblando una task force dedicata per andare dopo i crimini degli oligarchi russi. Stiamo fornendo più di un miliardo di dollari in assistenza diretta all'Ucraina e fornendo assistenza militare."],
# 'output_text': "\n\nQuesta sera, ci incontriamo come democratici, repubblicani e indipendenti, ma soprattutto come americani. La Russia di Putin ha cercato di scuotere le fondamenta del mondo libero, ma ha sottovalutato la forza della gente ucraina. Insieme ai nostri alleati, stiamo imponendo sanzioni economiche, tagliando l'accesso della Russia alla tecnologia, bloccando i suoi più grandi istituti bancari dal sistema finanziario internazionale e chiudendo lo spazio aereo americano a tutti i voli russi. Il Dipartimento di Giustizia degli Stati Uniti sta anche assemblando una task force dedicata per andare dopo i crimini degli oligarchi russi. Stiamo fornendo più di un miliardo di dollari in assistenza diretta all'Ucraina e fornendo assistenza militare."}

# The custom MapReduceChain
# Multi input prompt

# You can also use prompt with multi input. In this example, we will use a MapReduce chain to answer specific question about our code.

from langchain.chains.combine_documents.map_reduce import MapReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain

map_template_string = """Give the following python code information, generate a description that explains what the code does and also mention the time complexity.
Code:
{code}

Return the the description in the following format:
name of the function: description of the function
"""


reduce_template_string = """Given the following python function names and descriptions, answer the following question
{code_description}
Question: {question}
Answer:
"""

MAP_PROMPT = PromptTemplate(input_variables=["code"], template=map_template_string)
REDUCE_PROMPT = PromptTemplate(
    input_variables=["code_description", "question"], template=reduce_template_string
)

llm = OpenAI()

map_llm_chain = LLMChain(llm=llm, prompt=MAP_PROMPT)
reduce_llm_chain = LLMChain(llm=llm, prompt=REDUCE_PROMPT)

generative_result_reduce_chain = StuffDocumentsChain(
    llm_chain=reduce_llm_chain,
    document_variable_name="code_description",
)

combine_documents = MapReduceDocumentsChain(
    llm_chain=map_llm_chain,
    combine_document_chain=generative_result_reduce_chain,
    document_variable_name="code",
)

map_reduce = MapReduceChain(
    combine_documents_chain=combine_documents,
    text_splitter=CharacterTextSplitter(
        separator="\n##\n", chunk_size=100, chunk_overlap=0
    ),
)


code = """
def bubblesort(list):
   for iter_num in range(len(list)-1,0,-1):
      for idx in range(iter_num):
         if list[idx]>list[idx+1]:
            temp = list[idx]
            list[idx] = list[idx+1]
            list[idx+1] = temp
    return list
##
def insertion_sort(InputList):
   for i in range(1, len(InputList)):
      j = i-1
      nxt_element = InputList[i]
   while (InputList[j] > nxt_element) and (j >= 0):
      InputList[j+1] = InputList[j]
      j=j-1
   InputList[j+1] = nxt_element
   return InputList
##
def shellSort(input_list):
   gap = len(input_list) // 2
   while gap > 0:
      for i in range(gap, len(input_list)):
         temp = input_list[i]
         j = i
   while j >= gap and input_list[j - gap] > temp:
      input_list[j] = input_list[j - gap]
      j = j-gap
      input_list[j] = temp
   gap = gap//2
   return input_list

"""

map_reduce.run(input_text=code, question="Which function has a better time complexity?")

# Created a chunk of size 247, which is longer than the specified 100
# Created a chunk of size 267, which is longer than the specified 100

# 'shellSort has a better time complexity than both bubblesort and insertion_sort, as it has a time complexity of O(n^2), while the other two have a time complexity of O(n^2).'
