const express = require('express');
const { spawn } = require('child_process');
const axios = require('axios');
const WebSocket = require('ws');
const cors = require('cors'); // 引入 CORS 中间件
const { analyzeFailures } = require("./chat");
//"0x6a49f91230311b4823eeb0da26676c45ff41801a"
const path = '/mnt/c/Users/Jupiter/Desktop/Night Watcher/Formal Verification';
process.env.CERTORAKEY = "";

const app = express();
const port = 3000;

// 使用 CORS 中间件，允许来自前端的请求
app.use(cors({ origin: 'http://localhost:5173' }));

// 允许解析 JSON 请求体
app.use(express.json());

// 启动 HTTP 服务器
const server = app.listen(port, () => {
  console.log(`HTTP server running at http://localhost:${port}`);
});

// 启动 WebSocket 服务器
const wss = new WebSocket.Server({ port: 3001 }, () => {
  console.log('WebSocket server running at ws://localhost:3001');
});

// 处理前端发送的合约地址
app.post('/check-contract', (req, res) => {
  const { contractAddress } = req.body;

  if (!contractAddress) {
    return res.status(400).send({ error: 'Contract address is required' });
  }

  console.log(`Received contract address: ${contractAddress}`);

  let failuresLog = '';

  const certoraProcess = spawn('C:\\Windows\\System32\\wsl.exe', [
    'bash', '-c',
    `export CERTORAKEY=${process.env.CERTORAKEY} && cd "${path}" && /home/jupiter/.pyenv/shims/certoraRun certora/conf/amm/verify_amm_fetched.conf`
  ]);

  certoraProcess.stdout.setEncoding('utf8');
  certoraProcess.stderr.setEncoding('utf8');

  certoraProcess.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
    broadcastMessage({ type: 'log', message: data });
    if (data.includes('Failures summary')) failuresLog += data;
    if (data.includes('Failed on')) failuresLog += data;
    if (data.includes('Assert message')) failuresLog += data;
  });

  certoraProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
    broadcastMessage({ type: 'log', message: data });
  });

  certoraProcess.on('close', async (code) => {
    console.log(`Certora process exited with code ${code}`);
    console.log('Failures summary:', failuresLog);

    if (failuresLog) {
      console.log('Sending Failures summary to ChatGPT...');
      console.log(failuresLog);
      const analysis = await analyzeFailures(failuresLog);
      broadcastMessage({ type: 'analysis', message: analysis });
      console.log('ChatGPT Analysis:', analysis);
    }
  });

  res.send({ message: 'Contract analysis started' });
});

// 广播消息给所有 WebSocket 客户端
function broadcastMessage(data) {
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify(data));
    }
  });
}
