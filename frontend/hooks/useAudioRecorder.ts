import { useEffect, useRef, useState } from "react";

export function useAudioRecorder() {
  const [isRecording, setIsRecording] = useState(false);
  const [audioFile, setAudioFile] = useState<File | null>(null);
  const [duration, setDuration] = useState(0);
  const audioContext = useRef<AudioContext | null>(null);
  const analyser = useRef<AnalyserNode | null>(null);
  const animmationFrame = useRef<number | null>(null);

  const [audioLevel, setAudioLevel] = useState(0);

  const mediaRecorder = useRef<MediaRecorder | null>(null);
  const chunks = useRef<Blob[]>([]);
  const timer = useRef<number | null>(null);

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: true,
    });

    audioContext.current = new AudioContext();

    const source = audioContext.current.createMediaStreamSource(stream);

    analyser.current = audioContext.current.createAnalyser();

    analyser.current.fftSize = 256;

    source.connect(analyser.current);

    const recorder = new MediaRecorder(stream);
    mediaRecorder.current = recorder;

    chunks.current = [];

    analyserVoice();
    recorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        chunks.current.push(event.data);
      }
    };

    recorder.onstop = () => {
      const blob = new Blob(chunks.current, {
        type: "audio/webm",
      });
      const file = new File([blob], "recording.webm", {
        type: blob.type,
      });

      setAudioFile(file);

      stream.getAudioTracks().forEach((track) => track.stop());
    };

    recorder.start();
    setIsRecording(true);

    timer.current = window.setInterval(() => {
      setDuration((prev) => prev + 1);
    }, 1000);
  };

  const analyserVoice = () => {
    if (!analyser.current) return;

    const data = new Uint8Array(analyser.current.frequencyBinCount);

    analyser.current.getByteFrequencyData(data);

    const average = data.reduce((a, b) => a + b, 0) / data.length;

    setAudioLevel(average);

    animmationFrame.current = requestAnimationFrame(analyserVoice);
  };

  const stopRecording = () => {
    if (!mediaRecorder.current) return;

    mediaRecorder.current.stop();
    setIsRecording(false);

    if (animmationFrame.current) {
      cancelAnimationFrame(animmationFrame.current);
    }

    if (timer.current) {
      clearInterval(timer.current);
    }

    audioContext.current?.close();
  };

  const resetRecording = () => {
    setAudioFile(null);
    setDuration(0);
  };

  useEffect(() => {
    return () => {
      if (timer.current) {
        clearInterval(timer.current);
      }
    };
  }, []);

  return {
    isRecording,
    audioFile,
    duration,
    startRecording,
    stopRecording,
    resetRecording,
    audioLevel,
  };
}
