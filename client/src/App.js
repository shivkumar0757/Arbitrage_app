import React , {useState, useEffect} from 'react'

function App() {

  const [data, setData] = useState([{}])

  useEffect(() => {
    fetch("/list").then(
      res => res.json()
    ).then(data =>{
      setData(data)
      console.log(data)
    })
  },[]

  )
  return (
    <div>
      {(typeof data.data === 'undefined')?(
        <p>Loading...</p>
      ): (
        data.data.map((member,i)=>(
          <p key={i}> {member}</p>
        ))
      )}
    </div>
  )
}

export default App
