from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from groq import Groq

load_dotenv()


def main():
    print("Hello from langchain-course!")
    print(f"GROQ_API_KEY: {os.getenv('GROQ_API_KEY')}")
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    #print(client.models.list())
    information = """
            Elon Reeve Musk (/ˈiːlɒn/ EE-lon; born June 28, 1971) is a businessman and entrepreneur known for his leadership of Tesla, SpaceX, X, and xAI. Musk has been the wealthiest person in the world since 2025; as of February 2026, Forbes estimates his net worth to be around US$852 billion.

            Born into a wealthy family in Pretoria, South Africa, Musk emigrated in 1989 to Canada; he has Canadian citizenship since his mother was born there. He received bachelor's degrees in 1997 from the University of Pennsylvania before moving to California to pursue business ventures. In 1995, Musk co-founded the software company Zip2. Following its sale in 1999, he co-founded X.com, an online payment company that later merged to form PayPal, which was acquired by eBay in 2002. Musk also became an American citizen in 2002.
                  """

    summary =  """
            Given the {information} about a person, i want you to create:
            1. A short summary about him.
            2. two interest facts about him.
             3. A question about him.
             """
    prompt = PromptTemplate(input_variables=["information"],template=summary)
    llm = ChatGroq(model_name="llama-3.1-8b-instant",temperature=0.7)
    chain = prompt | llm
    response = chain.invoke(input={"information": information})
    print(response)
    
if __name__ == "__main__":
    main()
