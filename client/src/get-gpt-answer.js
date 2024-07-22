import axios from 'axios'

const getGPTAnswer = async (question) => {
  const response = await axios.post("http://localhost:5000/question", {question: question})

  return response.data
}

export default getGPTAnswer