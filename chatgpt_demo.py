import os
import openai

import streamlit as st
from streamlit.web.cli import main

def get_completion(key, model, max_tokens, temperature, content):
    """一个封装 OpenAI 接口的函数，参数为 Prompt，返回对应结果

    Args:
        prompt : 模型的输入列表
        model (str, optional): 模型的名称. 默认是"gpt-3.5-turbo".
        temperature (int, optional): Defaults to 0.2.

    Returns:
        response
    """

    # 创建一个 completion，并得到回答
    openai.api_key = key
    response = openai.ChatCompletion.create(
        model=model,
        messages=content,
        temperature=temperature, # 模型输出的温度系数，控制输出的随机程度
        max_tokens=max_tokens
    )

    print(response)
    # 返回回答文本内容
    return response.choices[0].message["content"]

st.set_page_config(page_title="ChatGPT机器人api部署")

with st.sidebar:
    st.title('范维设计-通过API与大模型的对话')
    st.text("最好使用自己的Token，管理员的Token在不同电脑上登录后会被禁掉")
    # st.write('支持的大模型包括的ChatGLM3和4')
    if 'API_TOKEN' in st.session_state and len(st.session_state['API_TOKEN']) > 1:
        st.success('API Token已经配置', icon='✅')
        key = st.session_state['API_TOKEN']
    else:
        key = ""

    key = st.text_input('输入Token:', type='password', value=key)

    st.session_state['API_TOKEN'] = key

    model = st.selectbox("选择模型", ["gpt-3.5-turbo", "gpt-4-turbo"])
    max_tokens = st.slider("max_tokens", 0, 2000, value=512)
    temperature = st.slider("temperature", 0.0, 2.0, value=0.8)

# 初始化的对话
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "你好我是ChatGPT，有什么可以帮助你的？"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "你好我是ChatGPT，有什么可以帮助你的？"}]

st.sidebar.button('清空聊天记录', on_click=clear_chat_history)


if len(key) > 1:
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("请求中..."):
                response = get_completion(key, model, max_tokens, temperature, st.session_state.messages)
                full_response = get_completion(key, model, max_tokens, temperature, st.session_state.messages)
                st.markdown(full_response)

                message = {"role": "assistant", "content": full_response}
                st.session_state.messages.append(message)

