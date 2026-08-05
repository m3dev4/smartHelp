
import { SupportTicketRequest, SupportTicketResponse } from "@/types/apiType";
import { useMutation } from "@tanstack/react-query";
import axios from "axios";

const createSupportTicket = async (data: SupportTicketRequest): Promise<SupportTicketResponse> => {
  const formData = new FormData();

  if (data.texte) {
    formData.append("description", data.texte);
  }

  if (data.AudioFile) {
    formData.append("audio", data.AudioFile);
  }

  if (data.ImageFile) {
    formData.append("image", data.ImageFile);
  }

  const response = await axios.post("http://127.0.0.1:8000/ingestions/support-ticket", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

export const useSupportTicket = () => {
  return useMutation({
    mutationFn: createSupportTicket,
  });
};
