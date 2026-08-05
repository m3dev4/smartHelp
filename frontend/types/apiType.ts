export interface SupportTicketRequest {
  texte?: string;
  AudioFile?: File | null;
  ImageFile?: File | null;
}

export interface DefectDetected {
  hasAnomaly: boolean;
  type: string;
  confidence: number;
  description: string;
}

export interface SupportTicketResponse {
  transcription: string;
  defect_detected: DefectDetected;
  policy_rule_applied: string;
  diagnostic_status: string;
}
