import streamlit as st
from agent.agent import Agent 

state = st.session_state

st.subheader("Conversa com o Assistente:")
st.markdown("""**Faça solicitações do tipo**:
- Quem deu mais passes na partida?
- Qual jogador teve mais finalizações no primeiro tempo?
- Compare o Jogador X e o Jogador Y.
- Gere um resumo da partida.
- Crie uma narrativa da partida em estilo formal/humorístico/técnico.""")
if state.selected_match is not None:  
    # Gerencia a habilitação/desabilitação do input no estado da aplicação
    if "input_disabled" not in state:
        state.input_disabled = False
    
    # Inicialização do LangChain Agent
    if "agent" not in state:
        state.agent = Agent(state.match_events, state.lineups, state.descricao_partida).create_agent()

    # Cria uma config para possibilitar a memória do Agente
    config = {"configurable": {"thread_id": "thread-1"}}

    # Histórico de mensagens
    if "messages" not in state:
        state.messages = []

    # Desabilita o input após enviar uma mensagem
    def disable_input():
        st.session_state.input_disabled = True

    # Interface de chat
    msg_container = st.container()
    prompt = st.chat_input("Faça uma pergunta ao assistente sobre a partida ou jogadores:", disabled=state.input_disabled, on_submit=disable_input)

    # Exibição do histórico
    for msg in state.messages:
        with msg_container:
            st.chat_message(msg["role"]).write(msg["content"])

    # Processamento do prompt
    if prompt:
        state.messages.append({"role": "user", "content": prompt})
        with msg_container:
            st.chat_message("user").write(prompt)

        try:
            input = {"messages": [("user", prompt)]}
            response = state.agent.invoke(input, config)['messages']
            # Você pode fazer o Debug da resposta do agente aqui:
            print(response, "\n\n")
            response = response[-1].content
            state.messages.append({"role": "assistant", "content": response})
            with msg_container:
                st.chat_message("assistant").write(response)
        except Exception as e:
            st.error(f"Erro ao processar sua solicitação: {e}")

        state.input_disabled = False
        st.rerun()
