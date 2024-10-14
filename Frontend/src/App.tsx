import { client } from "./client";
import { ConnectButton } from "thirdweb/react";
import { useEffect, useState, useRef } from "react";
import logoIcon from "./logo.jpg";
import ReactMarkdown from 'react-markdown';

export function App() {
  const [logs, setLogs] = useState([]);
  const [accountLogs, setAccountLogs] = useState([]);
  const [contractAddress, setContractAddress] = useState('');
  const [analysisReport, setAnalysisReport] = useState('报告生成中...');
  const [showReport, setShowReport] = useState(false);
  const [isChecking, setIsChecking] = useState(false);
  const logContainerRef = useRef(null);
  const [verificationLink, setVerificationLink] = useState(null);

  useEffect(() => {
	if(isChecking) {
    localStorage.setItem("accountLogs", JSON.stringify(accountLogs));
	}
  }, [accountLogs]);

  // WebSocket 连接和消息处理
  useEffect(() => {
	const socket = new WebSocket("ws://localhost:3001");
  
	socket.onopen = () => console.log("WebSocket connected");
  
	socket.onmessage = (event) => {
	  const data = JSON.parse(event.data);
	  setIsChecking(true);
  
	  setLogs((prevLogs) => [...prevLogs, { type: data.type, message: data.message }]);
  
	  // 检查是否有链接
	  const linkPattern = /https:\/\/prover\.certora\.com\/output\/\d+\/[a-f0-9]+\?anonymousKey=[a-f0-9]+/;
	  const foundLink = data.message.match(linkPattern)?.[0];
  
	  if (foundLink) {
		setVerificationLink(foundLink); // 存储链接
	  }
  
	  if (data.type === "analysis") {
		setAnalysisReport(data.message);
		setIsChecking(false);
	  }
	};
  
	socket.onerror = (error) => {
	  console.error("WebSocket error:", error);
	};
  
	socket.onclose = () => {
	  console.log("WebSocket disconnected");
	};
  
	return () => socket.close();
  }, []);


  // 自动滚动日志
  useEffect(() => {
    if (logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [logs, accountLogs]);

  // 异常检测按钮点击事件
  const handleCheck = async () => {
	if (!contractAddress) {
	  alert("请输入一个合约地址！");
	  return;
	}
	setIsChecking(true); 
	try {
	  const response = await fetch("http://localhost:3002/run-analysis", {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({ contractAddress }),
	  });
  
	  const result = await response.json();
	  console.log(result.output);
  
	  // 确保结构和 logs 一致
	  setAccountLogs([{message: result.output}]);
	} catch (error) {
	  console.error("Failed to start contract check:", error);
	}

	try {
		const response = await fetch("http://localhost:3000/check-contract", {
		  method: "POST",
		  headers: { "Content-Type": "application/json" },
		  body: JSON.stringify({ contractAddress }),
		});
	
		const result = await response.json();
		console.log(result.message);
		setLogs((prevLogs) => [...prevLogs, { type: 'log', message: '初始化过程中...' }]);
	  } catch (error) {
		console.error("Failed to start contract check:", error);
	  } 
  };

  // 渲染日志


  return (
    <main className="p-4 pb-10 min-h-[100vh] flex items-center justify-center container mx-auto w-full">
      <div className="py-10">
        <Header />

        <div className="flex justify-center mb-6">
          <ConnectButton client={client} appMetadata={{ name: "Example app", url: "https://example.com" }} />
        </div>

        <div className="flex items-center space-x-4 mb-10">
          <input
            type="text"
            value={contractAddress}
            onChange={(e) => setContractAddress(e.target.value)}
            placeholder="请输入合约地址"
            className="w-full p-5 rounded-lg bg-gray-900 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-violet-500"
          />
<button
  onClick={handleCheck}
  className="p-4 w-32 bg-violet-600 hover:bg-violet-700 text-white font-semibold rounded-lg"
  disabled={isChecking}
>
  {isChecking ? (
    <svg
      className="animate-spin h-5 w-5 text-white"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      ></circle>
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
      ></path>
    </svg>
  ) : (
    '异常检测'
  )}
</button>

        </div>

        <CommandLine title="异常账户检测" logs={accountLogs} logContainerRef={logContainerRef} />
        <CommandLine title="形式化合约验证" logs={logs} logContainerRef={logContainerRef} />

        <div className="flex justify-center mt-6">
          <button onClick={() => setShowReport(true)} className="p-4 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg mx-5">
            查看报告
          </button>
		  <button
  onClick={() => {
    if (verificationLink) {
      window.open(verificationLink, "_blank", "noopener,noreferrer");
    } else {
      alert("验证链接未找到");
    }
  }}
  className="p-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg mx-5"
>
  查看验证详情
</button>
        </div>
		

        {showReport && <ReportModal analysisReport={analysisReport} onClose={() => setShowReport(false)} />}
      </div>
    </main>
  );
}

const renderLog = (log, index) => {
	let color = "text-gray-300";
	if (log.type === "analysis") color = "text-green-400";
	if (log.type === "error") color = "text-red-500";
  
	return (
	  <div key={index} className={`whitespace-pre-wrap ${color} mb-2`}>
		{log.message}
	  </div>
	);
  };

// 命令行组件
// 命令行组件
function CommandLine({ title, logs, logContainerRef }) {
	return (
	  <div
		className="mt-10 p-4 bg-gray-800 rounded-lg max-h-48 overflow-y-auto relative"
		ref={logContainerRef}
	  >
		<h2 className="sticky top-[-16px] bg-gray-800 text-lg font-semibold mb-2 text-blue-300">
		  {title}
		</h2>
		<div className="text-sm">
		  {logs.map((log, index) => renderLog(log, index))}
		</div>
	  </div>
	);
  }
  


// 报告弹窗组件
function ReportModal({ analysisReport, onClose }) {
	return (
	  <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
		<div className="bg-white p-6 rounded-lg max-w-lg w-full max-h-[80vh] overflow-y-auto">
		  <h2 className="text-xl font-semibold mb-4 text-black">分析报告</h2>
		  {/* 使用 ReactMarkdown 渲染内容 */}
		  <div className="prose max-w-none text-black">
			<ReactMarkdown>{analysisReport}</ReactMarkdown>
		  </div>
		  <button
			onClick={onClose}
			className="mt-4 p-2 bg-red-600 hover:bg-red-700 text-white rounded-lg"
		  >
			关闭
		  </button>
		</div>
	  </div>
	);
  }

function Header() {
  return (
    <header className="flex flex-col items-center">
      <img
        src={logoIcon}
        alt="Logo"
        className="size-[150px] md:size-[150px] rounded-full mb-4"
        style={{ filter: "drop-shadow(0px 0px 24px #a8a632)" }}
      />
      <h1 className="text-2xl md:text-6xl font-bold tracking-tighter mb-6 text-zinc-100">
        Night's Watcher
      </h1>
    </header>
  );
}

