import React from "react";
import { Button } from "./ui/button";

interface AttachementItemProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  onClick: () => void;
}

const Attachement = ({ title, icon, description, onClick }: AttachementItemProps) => {
  return (
    <div className="flex gap-3 items-center w-full rounded-lg p-3">
      <Button onClick={onClick} className="w-full">
        {icon}
        <p className="text-medium">{title}</p>
        <p className="text-sm text-muted-foreground">{description}</p>
      </Button>
    </div>
  );
};

export default Attachement;
