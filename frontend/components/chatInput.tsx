import { useAudioRecorder } from "@/hooks/useAudioRecorder";
import React, { useEffect } from "react";
import { Button } from "./ui/button";
import { Mic, Pause } from "lucide-react";

interface ChatInputProps {
  className?: string;
  onRecordingComplete?: (file: File) => void;
}

const ChatInput = ({ className, onRecordingComplete }: ChatInputProps) => {
  const { isRecording, startRecording, stopRecording, audioLevel, audioFile } =
    useAudioRecorder();

  useEffect(() => {
    if (audioFile && onRecordingComplete) {
      onRecordingComplete(audioFile);
    }
  }, [audioFile, onRecordingComplete]);

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
