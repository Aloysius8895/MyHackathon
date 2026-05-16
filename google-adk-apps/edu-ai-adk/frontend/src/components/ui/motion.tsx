import React, { useEffect, useRef } from "react";

// Define proper TypeScript interfaces for the motion component props
interface MotionProps {
  children: React.ReactNode;
  initial?: {
    opacity?: number;
    y?: number;
    x?: number;
    scale?: number;
  };
  animate?: {
    opacity?: number;
    y?: number;
    x?: number;
    scale?: number;
  };
  transition?: {
    duration?: number;
    delay?: number;
    ease?: string;
  };
  className?: string;
  [key: string]: any; // Allow other props to be passed through
}

// Simple motion component to add animations without requiring framer-motion
export const motion = {
  div: ({
    children,
    initial = {},
    animate = {},
    transition = {},
    className = "",
    ...props
  }: MotionProps) => {
    const divRef = useRef<HTMLDivElement>(null);

    // Calculate easing function based on transition.ease
    const getEasingFunction = (ease: string = "easeOut") => {
      switch (ease) {
        case "linear":
          return "cubic-bezier(0, 0, 1, 1)";
        case "easeIn":
          return "cubic-bezier(0.42, 0, 1, 1)";
        case "easeOut":
          return "cubic-bezier(0, 0, 0.58, 1)";
        case "easeInOut":
          return "cubic-bezier(0.42, 0, 0.58, 1)";
        default:
          return "cubic-bezier(0, 0, 0.58, 1)"; // default to easeOut
      }
    };

    const initialStyles = {
      opacity: initial.opacity !== undefined ? initial.opacity : 1,
      transform: `translateY(${initial.y || 0}px) translateX(${
        initial.x || 0
      }px) scale(${initial.scale || 1})`,
      willChange: "opacity, transform",
    };

    const easing = getEasingFunction(transition.ease);

    const finalStyles = {
      opacity: animate.opacity !== undefined ? animate.opacity : 1,
      transform: `translateY(${animate.y || 0}px) translateX(${
        animate.x || 0
      }px) scale(${animate.scale || 1})`,
      transition: `opacity ${transition.duration || 0.5}s ${easing} ${
        transition.delay || 0
      }s, transform ${transition.duration || 0.5}s ${easing} ${
        transition.delay || 0
      }s`,
    };

    // Apply animation after component mounts using useEffect for smoother transition
    useEffect(() => {
      const timerId = setTimeout(() => {
        if (divRef.current) {
          Object.assign(divRef.current.style, {
            opacity: finalStyles.opacity,
            transform: finalStyles.transform,
            transition: finalStyles.transition,
          });
        }
      }, 50); // Small delay to ensure DOM is ready

      return () => clearTimeout(timerId);
    }, []);

    return (
      <div ref={divRef} className={className} style={initialStyles} {...props}>
        {children}
      </div>
    );
  },
};
