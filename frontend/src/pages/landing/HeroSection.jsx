import video1 from "../landing/assets/video4.webm";
import video2 from "../landing/assets/video6.webm";
import { useNavigate } from 'react-router-dom';
import { MessageCircle } from 'lucide-react';

const HeroSection = () => {
  const navigate = useNavigate();

  const handleChatClick = () => {
    navigate('/chat');
  };

  return (
    <div className="flex flex-col items-center mt-6 lg:mt-8">
      <h1 className="text-3xl sm:text-4xl lg:text-5xl text-center tracking-wide">
        FinWise :All Your Finances. <br></br>   
        <span className="bg-gradient-to-r from-blue-400 to-blue-800 text-transparent bg-clip-text">
          {" "}
               One Trusted Assistant.
        </span>
      </h1>
      <p className="mt-3 text-lg text-center text-neutral-500 max-w-4xl text-2xl">
      Empowering customers through intelligent, conversational finance.<br></br> 
      Our AI-driven chatbot simplifies personal loan journeys, from inquiry to sanction, in one seamless flow.<br></br> 
      A step toward intelligent, automated financial ecosystems.
      </p>
      <div className="flex justify-center my-10 ">
        <button className="px-6 py-3 bg-gradient-to-r from-sky-500 to-indigo-500 text-white font-semibold rounded-full shadow-md hover:shadow-lg hover:from-sky-600 hover:to-indigo-600 transition-all duration-300">
  Start for Free
</button>
        <a href="#" className="py-3 px-4 mx-3 rounded-md border hover:bg-blue-300">
          Documentation
        </a>
      </div>
      <div className="flex justify-center">
        <video
          autoPlay
          loop
          muted
          className="rounded-lg w-3/8 h-1/4 border border-blue-700 shadow-sm shadow-blue-400 mx-14 my-1"
        >
          <source src={video1} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
        <video
          autoPlay
          loop
          muted
          className="rounded-lg w-3/8 h-1/4 border border-blue-700 shadow-sm shadow-blue-400 mx-8 my-1"
        >
          <source src={video2} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      </div>

      {/* Floating Chat Popup */}
      <div className="fixed bottom-6 right-6 z-50 animate-bounce">
        <div 
          onClick={handleChatClick}
          className="bg-white rounded-2xl shadow-2xl p-4 max-w-xs relative border-2 border-blue-500 cursor-pointer hover:shadow-blue-300 hover:scale-105 transition-all duration-300"
        >
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-r from-sky-500 to-indigo-500 rounded-full p-3">
              <MessageCircle className="w-6 h-6 text-white" />
            </div>
            <div>
              <p className="font-semibold text-gray-800">Need help?</p>
              <p className="text-sm text-gray-600">Chat with us now!</p>
            </div>
          </div>
          {/* Notification dot with ping animation */}
          {/* <div className="absolute -top-1 -right-1 bg-red-500 rounded-full w-3 h-3 animate-ping"></div>
          <div className="absolute -top-1 -right-1 bg-red-500 rounded-full w-3 h-3"></div> */}
        </div>
      </div>
    </div>
  );
};

export default HeroSection;