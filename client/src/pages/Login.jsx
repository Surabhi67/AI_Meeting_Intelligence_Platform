import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

export const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();


  const handleLogin = async (e) => {
    e.preventDefault();


    try {
      const response = await fetch(
        "http://127.0.0.1:8000/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email,
            password,
          }),
        }
      );


      if (!response.ok) {
        throw new Error("Invalid credentials");
      }


      const data = await response.json();


      console.log("LOGIN:", data);


      localStorage.setItem(
        "token",
        data.access_token
      );


      navigate("/dashboard");


    } catch (error) {
      console.log(error);
      alert("Login failed");
    }
  };


  return (
    <div className="login-page">

      <div className="login-card">

        <h1>
          Welcome back
        </h1>

        <p>
          Sign in to continue to your meetings
        </p>


        <form
          onSubmit={handleLogin}
          className="login-form"
        >

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
          />


          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
          />


          <button type="submit">
            Login
          </button>


        </form>


        <div className="login-footer">
          <span>
            Don't have an account? Sign up
          </span>
        </div>


      </div>

    </div>
  );
};