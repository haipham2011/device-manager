export interface SystemDevice {
  id: number;
  code: string;
  name: string;
  size: string;
  weight: number;
  provider: string;
  description: string;
}
export interface SystemInfomation {
  version: string;
  company: string;
  location: string;
  system: {
    name: string;
    code: string;
    image: string;
    description: string;
  };
  devices: SystemDevice[];
}
