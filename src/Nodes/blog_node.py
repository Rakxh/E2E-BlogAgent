from src.State.blogstate import BlogState
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
    