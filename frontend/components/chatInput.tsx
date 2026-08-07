import { useAudioRecorder } from "@/hooks/useAudioRecorder";
import React, { useEffect, useRef } from "react";
import { Button } from "./ui/button";
import { Mic, Pause } from "lucide-react";

interface ChatInputProps {
  className?: string;
  onRecordingComplete?: (file: File) => void;
}

const ChatInput = ({ className, onRecordingComplete }: ChatInputProps) => {
  const { isRecording, startRecording, stopRecording, audioLevel, audioFile } =
    useAudioRecorder();

  // Use a ref for the callback to avoid triggering the effect on parent re-renders
  const onCompleteRef = useRef(onRecordingComplete);
  onCompleteRef.current = onRecordingComplete;

  useEffect(() => {
    if (audioFile && onCompleteRef.current) {
      onCompleteRef.current(audioFile);
    }
  }, [audioFile]);

  const toggleRecording = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  return (
    <>
      <Button
        type="button"
        variant="outline"
        size="icon"
        className={className}
        onClick={toggleRecording}
      >
        {isRecording ? <Pause /> : <Mic />}
      </Button>

      {isRecording && (
        <div className="absolute -top-10 left-1/2 -translate-x-1/2 bg-slate-100 rounded-lg px-4 py-1">
          <div
            className="w-1 rounded-full bg-primary"
            style={{ height: `${audioLevel}px`, }}
          />
        </div>
      )}
    </>
  );
};

export default ChatInput;

