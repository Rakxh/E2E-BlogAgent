from glob import translate
from src.State.blogstate import BlogState
from langchain_core.messages import HumanMessage, SystemMessage
from src.State.blogstate import Blog

class BlogNode:
    """
    A class to represent blog node
    """
    def __init__(self,llm):
        self.llm=llm
    
    def title_creation(self,state:BlogState):
        """
        Create the title for the blog
        """
        if "topic" in state and state['topic']:
            prompt="""
                    You are an expert blog content writer. Use the Markdown formatting. Generate a  catchy and professional blog
                    title for the {topic}. This title should be creative and SEO friendly. 
                   """
            sys_message=prompt.format(topic=state['topic'])
            response=self.llm.invoke(sys_message)
            return {"blog":{"title":response.content}}
    
    def content_gen(self,state:BlogState):
        if "topic" in state and state['topic']:
            prompt="""
                    You are an expert blog content writer. Use the Markdown formatting. Generate a detailed blog content with detailed breakdown
                    for the {topic}. 
                   """
            sys_message=prompt.format(topic=state['topic'])
            response=self.llm.invoke(sys_message)
            return {"blog":{"title":state["blog"]['title'],'content':response.content}}
    

    def translation(self,state:BlogState):
        """
        Translate the content to the specific language
        """

        translate_prompt="""
                         Translate the following content into {current_language}:
                         - Maintain the original tone, style and formatting.
                         - Adapt cultural references and idioms to be appropriate for {current_language}

                         ORIGINAL CONTENT:
                         {blog_content}

        """
        blog_content=state["blog"]["content"]

        messages=[HumanMessage(translate_prompt.format(current_language=state['current_language'],blog_content=blog_content))]

        translate_content=self.llm.with_structured_output(Blog).invoke(messages)

    def route(self,state):
        return{"current_language":state["current_language"]}
    
    def route_decision(self,state):
        """
        route the content to the respective translation function

        """
        if state['current_language']=='hindi':
            return 'hindi'
        
        elif state['current_language']=='french':
            return 'french'
        
        else:
            return state['current_language']