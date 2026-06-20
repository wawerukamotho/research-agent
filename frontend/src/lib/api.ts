import axios from 'axios';

export interface ResearchStatus {
  session_id: string;
  query: string;
  status: 'pending' | 'running' | 'finished' | 'failed';
  progress: number;
  current_task?: string;
  step_count: number;
  created_at: string;
  updated_at: string;
}

const BASE_URL = 'http://localhost:8000';

export const api = {
  async startResearch(params: { query: string }): Promise<ResearchStatus> {
    const response = await axios.post(`${BASE_URL}/research`, params);
    return response.data;
  },

  async getStatus(sessionId: string): Promise<ResearchStatus> {
    const response = await axios.get(`${BASE_URL}/research/${sessionId}`);
    return response.data;
  },

  getEventSource(sessionId: string): EventSource {
    return new EventSource(`${BASE_URL}/research/${sessionId}/events`);
  },

  getDownloadUrl(sessionId: string, format: 'pdf' | 'md' | 'docx' | 'json'): string {
    return `${BASE_URL}/research/${sessionId}/download/${format}`;
  }
};
