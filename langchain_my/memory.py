# from .model import create_model
# from .chain import create_base_chain, create_chain_lambda, create_chain_parallel, parallel_chain
# #########################################################################################################
# #########################################################################################################
# #########################################################################################################
# ######################### 임시 추가내용 - 메모리 저장1 - Automatic history
# from langgraph.checkpoint.memory import MemorySaver
# from langgraph.graph import START, MessagesState, StateGraph
# import streamlit as st
# from langchain_core.messages import SystemMessage
# ############################################################################
# from langchain_core.messages import trim_messages
# def trimmer():  # 대화내용 기억 위치 # 몇 전 대회까지 기억가능
#     trimmer = trim_messages(strategy="last", max_tokens=3, token_counter=len)
#     return trimmer
#                 # 대화내용 기억 위치 # 몇 전 대회까지 기억가능
# ############################################################################
# # Define the function that calls the model
# @st.cache_resource
# def call_model(state: MessagesState):
#                     # MessagesState 가 대신 기억
#     trimmed_messages = trimmer().invoke(state["messages"])
#     system_prompt = (
#         "You are a helpful assistant. "
#         "Answer all questions to the best of your ability."
#     )
#                                                     # state : defultfh "messages" 보유
#     messages = [SystemMessage(content=system_prompt)] + state["messages"]
#     # response = create_model().invoke(messages)
    
#     # parallel_chain 사용 시
#     response = create_chain_parallel(messages[-1].content)  # 마지막 메시지 내용만 전달
    
#     # 응답 형식 변환
#     if isinstance(response, dict) and "stock" in response and "issue" in response:
#         combined_content = f"{response['stock'].content}\n\n{response['issue'].content}"
#     else:
#         combined_content = str(response)
    
#     # 올바른 메시지 형식으로 반환
#     return {
#         "messages": [
#             {
#                 "role": "assistant",
#                 "content": combined_content
#             }
#         ]
#     }

# def create_workflow():
#     workflow = StateGraph(state_schema=MessagesState)

#     # Define the node and edge
#     workflow.add_node("model", call_model)
#     workflow.add_edge(START, "model")
#     workflow.add_edge("model", "model")  # 모델 노드를 자기 자신과 연결하여 대화 지속
#     # Add simple in-memory checkpointer
#     memory = MemorySaver()


#     app = workflow.compile(checkpointer=memory)
#     # >>> 해당 메머리 >> 기억하는 메모리 업그레이드
#     return app

# from IPython.display import Image
# from langchain_core.messages import HumanMessage

# def chat_with_memory(prompt: str):
    
    # app = create_workflow()
    # Image(app.get_graph().draw_mermaid_png())

    # # app invoke
    

    # # 첫 번째 질문
    # response = app.invoke(
    #     {"messages": [HumanMessage(content=prompt)]},
    #     config={"configurable": {"thread_id": "1"}}
    # )
    # print("First Response:", response["messages"][-1].content)
    # return response["messages"][-1].content

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
