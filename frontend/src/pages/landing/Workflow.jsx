import { CheckCircle2 } from "lucide-react";
import video3 from "../landing/assets/video8.webm";
import { checklistItems } from "../landing/constants";
import "./Workflow.css"; // Ensure this path is correct

const Workflow = () => {
  return (
    <div className="mt-8">
      <h2 className="text-3xl sm:text-2xl lg:text-5xl text-center mt-6 tracking-wide bounce-in">
        Our Smooth Process:{" "}
        <span className="bg-gradient-to-r from-blue-400 to-violet-800 text-transparent bg-clip-text">
          From Banking to Brilliance
        </span>
      </h2>
      <div className="flex flex-wrap justify-center">
        <div className="p-2 w-full lg:w-1/2">
          <video
            autoPlay
            loop
            muted
            className="rounded-lg w-1/2 h-132 border border-blue-700 shadow-sm shadow-blue-400 my-4 pulse"
          >
            <source src={video3} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
        <div className="pt-12 w-full lg:w-1/2">
          {checklistItems.map((item, index) => (
            <div
              key={index}
              className="flex mb-12 checklist-item"
            >
              <div className="text-blue-400 text-md bg-neutral-900 h-10 w-10 p-2 justify-center items-center rounded-full pulse">
                <CheckCircle2 />
              </div>
              <div>
                <h5 className="text-md bounce-in">{item.title}</h5>
                <p className="text-sm text-neutral-500 bounce-in">{item.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Workflow;
