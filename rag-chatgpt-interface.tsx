import { useState } from 'react';
import { Plus, Sun, Zap, AlertTriangle, Send, Menu, Settings, HelpCircle, LogOut, Lightbulb } from 'lucide-react';

export default function RAGChatInterface() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;
    
    const userMessage = { role: 'user', content: inputValue };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    
    // Simulate API call delay
    setTimeout(() => {
      const botMessage = { role: 'assistant', content: 'This is a simulated response from your RAG system. Connect this to your actual RAG API endpoint.' };
      setMessages(prev => [...prev, botMessage]);
      setIsLoading(false);
    }, 1000);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const examples = [
    "Explain quantum computing in simple terms",
    "Got any creative ideas for a 10 year old's birthday?",
    "How do I make an HTTP request in Javascript?"
  ];

  const capabilities = [
    "Remembers what user said earlier in the conversation",
    "Allows user to provide follow-up corrections",
    "Trained to decline inappropriate requests"
  ];

  const limitations = [
    "May occasionally generate incorrect information",
    "May occasionally produce harmful instructions or biased content",
    "Limited knowledge of world and events after 2021"
  ];

  return (
    <div className="flex h-screen bg-gray-800 text-white">
      {/* Sidebar */}
      <div className="w-64 bg-gray-900 flex flex-col">
        {/* New Chat Button */}
        <div className="p-3">
          <button className="w-full flex items-center gap-3 px-3 py-2 rounded-md border border-gray-600 hover:bg-gray-700 transition-colors">
            <Plus size={16} />
            <span className="text-sm">New chat</span>
          </button>
        </div>

        {/* Chat History */}
        <div className="flex-1 px-3">
          <div className="text-xs text-gray-400 mb-2">
            Your history will show up here. Not seeing what you expected? Try logging out and back in.
          </div>
        </div>

        {/* Bottom Menu */}
        <div className="p-3 border-t border-gray-700">
          <div className="space-y-1">
            <button className="w-full flex items-center gap-3 px-3 py-2 rounded-md hover:bg-gray-700 transition-colors text-sm">
              <Lightbulb size={16} />
              <span>Upgrade to Plus</span>
              <span className="ml-auto bg-yellow-500 text-black px-2 py-0.5 rounded text-xs font-medium">NEW</span>
            </button>
            <button className="w-full flex items-center gap-3 px-3 py-2 rounded-md hover:bg-gray-700 transition-colors text-sm">
              <Sun size={16} />
              <span>Light mode</span>
            </button>
            <button className="w-full flex items-center gap-3 px-3 py-2 rounded-md hover:bg-gray-700 transition-colors text-sm">
              <Settings size={16} />
              <span>Updates & FAQ</span>
            </button>
            <button className="w-full flex items-center gap-3 px-3 py-2 rounded-md hover:bg-gray-700 transition-colors text-sm">
              <LogOut size={16} />
              <span>Log out</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-center p-4 border-b border-gray-700">
          <h1 className="text-2xl font-semibold">RAG Assistant</h1>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto">
          {messages.length === 0 ? (
            /* Welcome Screen */
            <div className="h-full flex flex-col items-center justify-center px-4">
              <div className="max-w-4xl w-full">
                <div className="grid md:grid-cols-3 gap-6 mb-8">
                  {/* Examples */}
                  <div className="text-center">
                    <div className="w-12 h-12 bg-gray-700 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Sun size={20} />
                    </div>
                    <h3 className="text-lg font-medium mb-4">Examples</h3>
                    <div className="space-y-2">
                      {examples.map((example, index) => (
                        <button
                          key={index}
                          onClick={() => setInputValue(example)}
                          className="block w-full p-3 bg-gray-700 hover:bg-gray-600 rounded-md text-sm text-left transition-colors"
                        >
                          "{example}" →
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Capabilities */}
                  <div className="text-center">
                    <div className="w-12 h-12 bg-gray-700 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Zap size={20} />
                    </div>
                    <h3 className="text-lg font-medium mb-4">Capabilities</h3>
                    <div className="space-y-2">
                      {capabilities.map((capability, index) => (
                        <div key={index} className="p-3 bg-gray-700 rounded-md text-sm">
                          {capability}
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Limitations */}
                  <div className="text-center">
                    <div className="w-12 h-12 bg-gray-700 rounded-full flex items-center justify-center mx-auto mb-4">
                      <AlertTriangle size={20} />
                    </div>
                    <h3 className="text-lg font-medium mb-4">Limitations</h3>
                    <div className="space-y-2">
                      {limitations.map((limitation, index) => (
                        <div key={index} className="p-3 bg-gray-700 rounded-md text-sm">
                          {limitation}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            /* Chat Messages */
            <div className="max-w-4xl mx-auto w-full">
              {messages.map((message, index) => (
                <div key={index} className={`p-6 ${message.role === 'assistant' ? 'bg-gray-700' : ''}`}>
                  <div className="flex gap-4">
                    <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center flex-shrink-0">
                      {message.role === 'user' ? '👤' : '🤖'}
                    </div>
                    <div className="flex-1">
                      <div className="whitespace-pre-wrap">{message.content}</div>
                    </div>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="p-6 bg-gray-700">
                  <div className="flex gap-4">
                    <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center flex-shrink-0">
                      🤖
                    </div>
                    <div className="flex-1">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="p-4 border-t border-gray-700">
          <div className="max-w-4xl mx-auto">
            <div className="relative">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Send a message..."
                className="w-full p-4 pr-12 bg-gray-700 rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none resize-none"
                rows="1"
                style={{minHeight: '56px'}}
              />
              <button
                onClick={handleSendMessage}
                disabled={!inputValue.trim() || isLoading}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 p-2 bg-gray-600 hover:bg-gray-500 disabled:bg-gray-700 disabled:cursor-not-allowed rounded-md transition-colors"
              >
                <Send size={16} />
              </button>
            </div>
            <div className="text-xs text-gray-400 text-center mt-2">
              RAG Assistant. Your AI assistant powered by retrieval-augmented generation.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}