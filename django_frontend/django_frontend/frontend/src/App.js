import React, { useState } from "react";
import Form from "./components/Form";
import Result from "./components/Result";

function App() {
  const [result, setResult] = useState(null);

  return (<div className="container mt-5"> <h1 className="text-center">AI Fitness App</h1>
    <Form setResult={setResult} />
    <Result result={result} />
  </div>

);
}

export default App;
