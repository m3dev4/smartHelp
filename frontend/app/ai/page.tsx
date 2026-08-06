"use client";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import React, { useRef, useState } from "react";
import {
  Bot,
  CheckCircle2,
  FileText,
  ImageIcon,
  Loader,
  Mic,
  Paperclip,
  Scale,
  Send,
  Stethoscope,
} from "lucide-react";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import Attachement from "@/components/attachement";
import { useSupportTicket } from "@/hooks/useTicket";
import ResultRow from "@/components/resultRow";
import TypingWritter from "@/components/typingWritter";
import ChatInput from "@/components/chatInput";

const Support = () => {
  const audioRef = useRef<HTMLInputElement>(null);
  const imageRef = useRef<HTMLInputElement>(null);
  const [texte, setTexte] = useState("");
  const [AudioFile, setAudioFile] = useState<File | null>(null);
  const [ImageFile, setImageFile] = useState<File | null>(null);

  const supportMutateTicket = useSupportTicket();

  const handleAudioSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) setAudioFile(file);
  };

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) setImageFile(file);
  };

  const handleData = () => {
    supportMutateTicket.mutate({
      texte,
      AudioFile,
      ImageFile,
    });
  };

  return (
    <section className="h-screen relative w-full">
      <div className="flex items-center justify-center h-full">
        <div className="absolute bottom-0 mb-15 flex items-center justify-center w-full">
          <div className="flex-1">
            <div className="relative flex items-center w-full max-w-2xl mx-auto">
              <Popover>
                <PopoverTrigger asChild>
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    className="absolute left-1 top-2 rounded-full bg-background hover:bg-muted cursor-pointer"
                  >
                    <Paperclip className="text-amber-400 size-4" />
                  </Button>
                </PopoverTrigger>

                <PopoverContent
                  className="w-64 p-2 flex flex-col gap-1"
                  align="start"
                  side="top"
                >
                  <Attachement
                    icon={<Mic className="size-4 text-rose-500" />}
                    title="Audio"
                    description="MP3, WAV"
                    onClick={() => audioRef.current?.click()}
                  />
                  <Attachement
                    icon={<ImageIcon className="size-4 text-emerald-500" />}
                    title="Image"
                    description="PNG, JPG"
                    onClick={() => imageRef.current?.click()}
                  />

                  <input
                    ref={audioRef}
                    type="file"
                    accept="audio/mp3,audio/wav,audio/*"
                    className="hidden"
                    onChange={handleAudioSelect}
                  />
                  <input
                    ref={imageRef}
                    type="file"
                    accept="image/png,image/jpeg,image/*"
                    className="hidden"
                    onChange={handleImageSelect}
                  />
                </PopoverContent>
              </Popover>

              <Input
                className="w-full h-12 pl-12 pr-12 rounded-full border border-primary outline-none focus-visible:bg-slate-100 focus-visible:ring-2 focus-visible:ring-primary/40 transition-colors"
                placeholder="Écris un message..."
                value={texte}
                onChange={(e) => setTexte(e.target.value)}
              />

              <Button
                type="submit"
                size="icon"
                className="absolute right-1 top-2 rounded-full bg-primary hover:bg-primary/90 text-primary-foreground cursor-pointer"
                onClick={handleData}
                disabled={supportMutateTicket.isPending || ( !texte && !AudioFile && !ImageFile)}
              >
                {supportMutateTicket.isPending ? (
                  <Loader className="size-4 animate-spin" />
                ) : (
                  <Send className="size-4" />
                )}
              </Button>

              <ChatInput className="absolute right-12 top-2 rounded-full" onRecordingComplete={(file) => setAudioFile(file)} />
            </div>
          </div>
        </div>
        {/* response */}
        {supportMutateTicket.isSuccess && supportMutateTicket.data && (
          <div className="absolute top-1/3 -translate-y-1/2 left-1/2 -translate-x-1/2 w-full max-w-lg px-4">
            <div className=" backdrop-blur-sm rounded-2xl shadow-xl p-6 space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-300">
              <div className="flex items-center gap-2 pb-2 border-b border-slate-100">
                <CheckCircle2 className="size-5 text-emerald-500" />
                <h3 className="font-semibold text-slate-100">
                  Résultat de l'analyse
                </h3>
              </div>

              <ResultRow
                icon={<FileText className="size-4 text-blue-500" />}
                label="Transcription"
                value={
                  <TypingWritter
                    texte={supportMutateTicket.data?.transcription || ""}
                    speed={20}
                  />
                }
              />
              <ResultRow
                icon={<ImageIcon className="size-4 text-emerald-500" />}
                label="Image"
                value={
                  <TypingWritter
                    texte={
                      supportMutateTicket.data?.defect_detected?.type || ""
                    }
                    speed={20}
                  />
                }
              />
              <ResultRow
                icon={<Scale className="size-4 text-amber-500" />}
                label="Règlement intérieur"
                value={
                  <TypingWritter
                    texte={supportMutateTicket.data?.policy_rule_applied || ""}
                    speed={20}
                  />
                }
              />
              <ResultRow
                icon={<Stethoscope className="size-4 text-rose-500" />}
                label="Diagnostic"
                value={
                  <TypingWritter
                    texte={supportMutateTicket.data?.diagnostic_status || ""}
                    speed={20}
                  />
                }
              />
            </div>
          </div>
        )}
      </div>
    </section>
  );
};

export default Support;
