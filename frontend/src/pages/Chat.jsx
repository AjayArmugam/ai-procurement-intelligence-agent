import {
  useState,
  useRef,
  useEffect
} from "react";

import api from "../services/api";
import { Plus } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function Chat() {

  const [question, setQuestion] =
    useState("");

  const [messages, setMessages] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  const [selectedFile, setSelectedFile] =
  useState(null);

  const chatRef = useRef(null);

  const fileInputRef = useRef(null);

  const [uploadMessage, setUploadMessage] =
  useState("");

  const [uploading, setUploading] =
    useState(false);

  useEffect(() => {

    if (chatRef.current) {

      chatRef.current.scrollTop =
        chatRef.current.scrollHeight;

    }

  }, [messages, loading]);

  const newChat = () => {

    setMessages([]);
    setQuestion("");
    setSelectedFile(null);
    setUploadMessage("");

  };
  
  const uploadFile = async () => {

    if (!selectedFile) {
      return;
    }

    setUploading(true);

    const formData =
      new FormData();

    formData.append(
      "file",
      selectedFile
    );

    try {

      const response =
        await api.post(
          "/upload",
          formData,
          {
            headers: {
              "Content-Type":
                "multipart/form-data"
            }
          }
        );

      setUploadMessage(
        response.data.message
      );

      setTimeout(() => {

        setUploadMessage("");

      }, 3000);

    } catch (error) {

      console.error(error);

      setUploadMessage(
        "Upload failed."
      );

    } finally {

      setUploading(false);

    }

  };

  const sendQuestion = async () => {

    if (
      !question.trim() ||
      loading
    ) {
      return;
    }

    const currentQuestion =
      question;

    const userMessage = {
      role: "user",
      content: currentQuestion
    };

    setMessages((prev) => [
      ...prev,
      userMessage
    ]);

    setQuestion("");

    setLoading(true);

    try {

      const response =
        await api.post(
          "/query",
          {
            question:
              currentQuestion
          }
        );

      const aiMessage = {
        role: "assistant",
        content:
          response.data.answer
      };

      setMessages((prev) => [
        ...prev,
        aiMessage
      ]);

    } catch (error) {

      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Error contacting AI Agent."
        }
      ]);

    } finally {

      setLoading(false);

    }

  };

  const examplePrompts = [

    "Which vendor has the highest spend?",

    "What is the status of invoice INV-1002?",

    "Show details of invoice INV-9999",

    "How many invoices are pending?"

  ];

  return (

    <div
      style={{
        marginTop: "50px",
        padding: "20px",
        maxWidth: "1200px",
        marginLeft: "auto",
        marginRight: "auto"
      }}
    >

      <div
        style={{
          display: "flex",
          justifyContent:
            "space-between",
          alignItems: "center",
          marginBottom: "20px"
        }}
      >

        <div>

          <h2
            style={{
              fontSize: "34px",
              marginBottom: "8px"
            }}
          >
            Procurement Intelligence Assistant
          </h2>

          <p
            style={{
              color: "#94a3b8"
            }}
          >
            AI-powered invoice,
            vendor and spend
            analysis
          </p>

        </div>
        
       <input
            type="file"
            accept=".pdf,.txt"
            ref={fileInputRef}
            style={{
              display: "none"
            }}
            onChange={(e) => {

              setSelectedFile(
                e.target.files[0]
              );

            }}
         />

        <button
          onClick={newChat}
          style={{
            background:
              "#1e293b",

            color:
              "#ffffff",

            border:
              "1px solid #334155",

            padding:
              "12px 18px",

            borderRadius:
              "12px",

            cursor:
              "pointer",

            fontWeight:
              "bold",

            transition:
              "all 0.3s ease",

            boxShadow:
              "0 0 15px rgba(59,130,246,0.2)"
          }}
        >
          + New Chat
        </button>

      </div>

      <div
        ref={chatRef}
        style={{
          background:
            "#151824",

          borderRadius:
            "16px",

          padding:
            "25px",

          height:
            "500px",

          overflowY:
            "auto",

          marginBottom:
            "20px",

          border:
            "1px solid #2a2f45",

          boxShadow:
            "0 0 25px rgba(59,130,246,0.15)"
        }}
      >

        {messages.length === 0 &&
        !loading ? (

          <div
            style={{
              textAlign:
                "center",

              marginTop:
                "40px",

              color:
                "#94a3b8"
            }}
          >

            <h3
              style={{
                fontSize:
                  "28px",

                color:
                  "#ffffff",

                marginBottom:
                  "10px"
              }}
            >
              Welcome 👋
            </h3>

            <p
              style={{
                marginBottom:
                  "25px"
              }}
            >
              Ask questions about
              invoices, vendors
              and procurement
              analytics.
            </p>

            <div
              style={{
                display:
                  "flex",

                flexWrap:
                  "wrap",

                justifyContent:
                  "center",

                gap:
                  "10px"
              }}
            >

              {examplePrompts.map(
                (prompt) => (

                  <button
                    key={prompt}
                    onClick={() =>
                      setQuestion(
                        prompt
                      )
                    }
                    style={{
                      background:
                        "#1e293b",

                      border:
                        "1px solid #334155",

                      color:
                        "#cbd5e1",

                      padding:
                        "10px 14px",

                      borderRadius:
                        "10px",

                      cursor:
                        "pointer"
                    }}
                  >
                    {prompt}
                  </button>

                )
              )}

            </div>

          </div>

        ) : (

          <>
            {messages.map(
              (
                msg,
                index
              ) => (

                <div
                  key={index}
                  style={{
                    display:
                      "flex",

                    justifyContent:
                      msg.role ===
                      "user"
                        ? "flex-end"
                        : "flex-start",

                    marginBottom:
                      "15px"
                  }}
                >

                  <div
                    style={{
                      maxWidth:
                        msg.role === "assistant"
                           ? "85%"
                           : "60%",
                      textAlign:
                        msg.role === "assistant"
                          ? "left"
                          : "center",

                      padding:
                        "14px 18px",

                      borderRadius:
                        "16px",

                      background:
                        msg.role ===
                        "user"
                          ? "#2563eb"
                          : "#111827",

                      color:
                        "#ffffff",

                      lineHeight:
                        "1.7",

                      boxShadow:
                        msg.role ===
                        "user"
                          ? "0 0 20px rgba(37,99,235,0.4)"
                          : "0 0 15px rgba(255,255,255,0.05)"
                    }}
                  >
                    <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        components={{
                          h1: ({ children }) => (
                            <h1
                              style={{
                                color: "#60a5fa",
                                fontSize: "24px",
                                marginBottom: "15px"
                              }}
                            >
                              {children}
                            </h1>
                          ),

                          h2: ({ children }) => (
                            <h2
                              style={{
                                color: "#60a5fa",
                                fontSize: "20px",
                                marginBottom: "12px"
                              }}
                            >
                              {children}
                            </h2>
                          ),

                          p: ({ children }) => (
                            <p
                              style={{
                                marginBottom: "10px"
                              }}
                            >
                              {children}
                            </p>
                          ),

                          li: ({ children }) => (
                            <li
                              style={{
                                marginBottom: "6px"
                              }}
                            >
                              {children}
                            </li>
                          )
                        }}
                      >
                        {msg.content || ""}
                    </ReactMarkdown>

                  </div>

                </div>

              )
            )}

            {loading && (

              <div>

                <div
                  style={{
                    background:
                      "#1e293b",

                    padding:
                      "14px 18px",

                    borderRadius:
                      "16px",

                    color:
                      "#ffffff",

                    width:
                      "fit-content"
                  }}
                >
                  🔍 Analyzing procurement data...
                </div>

              </div>

            )}

          </>

        )}

      </div>

      {selectedFile && (

        <div
          style={{
            marginBottom: "15px",

            background: "#1e293b",

            border:
              "1px solid #334155",

            borderRadius: "12px",

            padding: "12px 16px",

            display: "flex",

            justifyContent:
              "space-between",

            alignItems: "center",

            color: "#ffffff"
          }}
        >

          <div>
            📄 {selectedFile.name}
          </div>

          <div
            style={{
              display: "flex",
              gap: "10px"
            }}
          >

            <button
              onClick={() => {

                setSelectedFile(
                  null
                );

              }}
              style={{
                background:
                  "#374151",

                color:
                  "white",

                border:
                  "none",

                padding:
                  "8px 12px",

                borderRadius:
                  "8px",

                cursor:
                  "pointer"
              }}
            >
              Cancel
            </button>

            <button
              onClick={uploadFile}
              disabled={
                uploading
              }
              style={{
                background:
                  "#2563eb",

                color:
                  "white",

                border:
                  "none",

                padding:
                  "8px 12px",

                borderRadius:
                  "8px",

                cursor:
                  "pointer"
              }}
            >
              {uploading
                ? "Uploading..."
                : "Upload"}
            </button>

          </div>

        </div>

      )} 

      {
  uploadMessage && (

      <div
        style={{
          marginBottom: "15px",
          padding: "12px",
          borderRadius: "10px",
          background:
            uploadMessage.includes(
              "exists"
            )
              ? "#78350f"
              : "#064e3b",
          color: "white"
        }}
      >
        {uploadMessage.includes(
          "exists"
        )
          ? "⚠️"
          : "✅"} {uploadMessage}
      </div>

    )
  }

      <div
        style={{
          display: "flex",
          gap: "10px",
          justifyContent: "center",
          alignItems: "center"
        }}
      >

        
        <button
                onClick={() => {

                  fileInputRef.current?.click();

                }}
                style={{
                  width: "50px",
                  height: "50px",

                  borderRadius: "50%",

                  border: "1px solid #334155",

                  background: "#1e293b",

                  color: "white",

                  cursor: "pointer",

                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",

                  transition: "all 0.3s ease",

                  boxShadow:
                    "0 0 15px rgba(59,130,246,0.2)"
                }}
                onMouseEnter={(e) => {

                  e.currentTarget.style.boxShadow =
                    "0 0 25px rgba(59,130,246,0.7)";

                  e.currentTarget.style.transform =
                    "scale(1.1)";

                }}
                onMouseLeave={(e) => {

                  e.currentTarget.style.boxShadow =
                    "0 0 15px rgba(59,130,246,0.2)";

                  e.currentTarget.style.transform =
                    "scale(1)";

                }}
              >
                <Plus size={20} />
          </button>
        <input
          type="text"
          value={question}
          onChange={(e) =>
            setQuestion(
              e.target.value
            )
          }
          onKeyDown={(e) => {

            if (
              e.key ===
                "Enter" &&
              !loading
            ) {

              sendQuestion();

            }

          }}
          placeholder="Ask a procurement question..."
          style={{
            width:
              "900px",

            padding:
              "14px",

            borderRadius:
              "10px",

            border:
              "1px solid #334155",

            background:
              "#111827",

            color:
              "#ffffff",

            fontSize:
              "16px"
          }}
        />

        <button
          onClick={
            sendQuestion
          }
          disabled={
            loading
          }
          style={{
            padding:
              "14px 28px",

            borderRadius:
              "12px",

            border:
              "none",

            background:
              "linear-gradient(135deg,#2563eb,#06b6d4)",

            color:
              "white",

            fontWeight:
              "bold",

            fontSize:
              "15px",

            cursor:
              loading
                ? "not-allowed"
                : "pointer",

            transition:
              "all 0.3s ease",

            boxShadow:
              "0 0 20px rgba(37,99,235,0.4)"
          }}
          onMouseEnter={(e) => {

            e.target.style.boxShadow =
              "0 0 35px rgba(59,130,246,0.9)";

            e.target.style.transform =
              "translateY(-2px) scale(1.03)";

          }}
          onMouseLeave={(e) => {

            e.target.style.boxShadow =
              "0 0 20px rgba(37,99,235,0.4)";

            e.target.style.transform =
              "translateY(0px) scale(1)";

          }}
        >
          {loading
            ? "Analyzing..."
            : "➤ Send"}
        </button>

      </div>

    </div>

  );

}

export default Chat;