import { useEffect, useRef, useState } from "react";

/**
 * Converts a WebM audio blob to WAV format using the Web Audio API.
 * Whisper hallucinates (repeats random phrases) with WebM input,
 * but handles WAV natively without issues.
 */
async function convertBlobToWav(blob: Blob): Promise<Blob> {
  const arrayBuffer = await blob.arrayBuffer();
  const audioCtx = new AudioContext();
  const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);

  const numChannels = 1; // mono
  const sampleRate = audioBuffer.sampleRate;
  const samples = audioBuffer.getChannelData(0);
  const buffer = new ArrayBuffer(44 + samples.length * 2);
  const view = new DataView(buffer);

  // WAV header
  const writeString = (offset: number, str: string) => {
    for (let i = 0; i < str.length; i++) {
      view.setUint8(offset + i, str.charCodeAt(i));
    }
  };

  writeString(0, "RIFF");
  view.setUint32(4, 36 + samples.length * 2, true);
  writeString(8, "WAVE");
  writeString(12, "fmt ");
  view.setUint32(16, 16, true); // PCM chunk size
  view.setUint16(20, 1, true); // PCM format
  view.setUint16(22, numChannels, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * numChannels * 2, true); // byte rate
  view.setUint16(32, numChannels * 2, true); // block align
  view.setUint16(34, 16, true); // bits per sample
  writeString(36, "data");
  view.setUint32(40, samples.length * 2, true);

  // Write PCM samples
  let offset = 44;
  for (let i = 0; i < samples.length; i++) {
    const s = Math.max(-1, Math.min(1, samples[i]));
    view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7fff, true);
    offset += 2;
  }

  await audioCtx.close();
  return new Blob([buffer], { type: "audio/wav" });
}

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

    recorder.onstop = async () => {
      const webmBlob = new Blob(chunks.current, {
        type: "audio/webm",
      });

      // Convert WebM → WAV to avoid Whisper hallucinations
      try {
        const wavBlob = await convertBlobToWav(webmBlob);
        const file = new File([wavBlob], "recording.wav", {
          type: "audio/wav",
        });
        setAudioFile(file);
      } catch {
        // Fallback to WebM if conversion fails
        const file = new File([webmBlob], "recording.webm", {
          type: webmBlob.type,
        });
        setAudioFile(file);
      }

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

