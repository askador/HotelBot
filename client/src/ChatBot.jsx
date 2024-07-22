import React, { useState } from "react"
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css"
import logo from './logo.png'
import getGPTAnswer from './get-gpt-answer'
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  TypingIndicator,
} from "@chatscope/chat-ui-kit-react"
import "./ChatBot.css"

const initialMessage = {
  message:
    "Hello, I'm HotelBot! Ask anything about our Hotel 5⭐️!",
  sentTime: "just now",
  sender: "HotelBot",
}

const processAnswer = (text) => {
  let processedText = String(text).trim()
  return processedText
}

export default function ChatBot() {
  const [isTyping, setIsTyping] = useState(false)
  const [messages, setMessages] = useState([initialMessage])

  const handleSend = async (message, textContent, innerText, nodes) => {
    const newMessage = {
      message,
      direction: "outgoing",
      sender: "user",
    }

    const newMessages = [...messages, newMessage]

    setMessages(prev => newMessages)

    setIsTyping(true)
    
    const answer = processAnswer(await getGPTAnswer(innerText))

    setIsTyping(false)

    setMessages(prevMessages => [...prevMessages, {
        message: answer,
        sender: "HotelBot",
    }])

  }

  return (
    <div className="chat">
      <div className="logo">
        <span>HotelBot</span>
        <img src={logo} alt=''/>
      </div>
      <div style={{ position: "relative", height: "660px", width: "700px" }}>
        <MainContainer className="main-container">
          <ChatContainer>
            <MessageList
              scrollBehavior="smooth"
              typingIndicator={
                isTyping ? (
                  <TypingIndicator content="HotelBot is thinking" />
                ) : null
              }
            >
              {messages.map((message, i) => {
                return <Message key={i} model={message} className="message-item" style={{"fontSize": "22px", "padding-top": "5px"}}/>
              })}
            </MessageList>
            <MessageInput placeholder="Type question here" onSend={handleSend} autoFocus={true} attachButton={false} style={{"fontSize": "20px"}}/>
          </ChatContainer>
        </MainContainer>
      </div>
    </div>
  )
}
