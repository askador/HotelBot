async function processMessageToChatGPT(chatMessages) { // messages is an array of messages
  // Format messages for chatGPT API
  // API is expecting objects in format of { role: "user" or "assistant", "content": "message here"}
  // So we need to reformat

  let apiMessages = chatMessages.map((messageObject) => {
    let role = "";
    if (messageObject.sender === "HotelBot") {
      role = "assistant";
    } else {
      role = "user";
    }
    return { role: role, content: messageObject.message}
  });




  // Get the request body set up with the model we plan to use
  // and the messages which we formatted above. We add a system message in the front to'
  // determine how we want chatGPT to act. 
  const apiRequestBody = {
    "model": "gpt-3.5-turbo",
    "messages": [
      systemMessage,  // The system message DEFINES the logic of our chatGPT
      ...apiMessages // The messages from our chat with ChatGPT
    ]
  }

  await fetch("https://api.openai.com/v1/chat/completions", 
  {
    method: "POST",
    headers: {
      "Authorization": "Bearer " + API_KEY,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(apiRequestBody)
  }).then((data) => {
    return data.json();
  }).then((data) => {
    console.log(data);
    setMessages([...chatMessages, {
      message: data.choices[0].message.content,
      sender: "ChatGPT"
    }]);
    setIsTyping(false);
  });
}
