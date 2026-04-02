---
name: user-onboarding
description: User onboarding flow design. "온보딩", "튜토리얼", "가이드", "신규 사용자" triggers this.
tools:
  - Read
  - Write
  - Edit
---

# User Onboarding Skill

## Triggers
- "온보딩", "튜토리얼", "가이드"
- "신규 사용자", "첫 사용", "시작하기"
- "onboarding", "welcome flow"

## Onboarding Principles

### Time to Value (TTV)
```yaml
goal: Get users to "aha moment" ASAP
strategies:
  - Skip non-essential steps
  - Pre-fill defaults
  - Show progress indicator
  - Celebrate wins
```

### Progressive Disclosure
```yaml
principle: Show only what's needed now
implementation:
  - Start simple, reveal complexity
  - Use tooltips for advanced features
  - Defer settings to later
```

## Onboarding Patterns

### Setup Wizard
```tsx
'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';

const steps = [
  { id: 'profile', title: 'Create your profile' },
  { id: 'workspace', title: 'Set up workspace' },
  { id: 'invite', title: 'Invite team' },
  { id: 'complete', title: 'You\'re all set!' },
];

export function OnboardingWizard() {
  const [currentStep, setCurrentStep] = useState(0);
  const progress = ((currentStep + 1) / steps.length) * 100;

  return (
    <div className="max-w-2xl mx-auto p-8">
      {/* Progress */}
      <div className="mb-8">
        <div className="flex justify-between text-sm mb-2">
          <span>Step {currentStep + 1} of {steps.length}</span>
          <span>{steps[currentStep].title}</span>
        </div>
        <Progress value={progress} />
      </div>

      {/* Step Content */}
      <div className="min-h-[300px]">
        {currentStep === 0 && <ProfileStep />}
        {currentStep === 1 && <WorkspaceStep />}
        {currentStep === 2 && <InviteStep />}
        {currentStep === 3 && <CompleteStep />}
      </div>

      {/* Navigation */}
      <div className="flex justify-between mt-8">
        <Button
          variant="ghost"
          onClick={() => setCurrentStep(s => s - 1)}
          disabled={currentStep === 0}
        >
          Back
        </Button>

        {currentStep < steps.length - 1 ? (
          <Button onClick={() => setCurrentStep(s => s + 1)}>
            Continue
          </Button>
        ) : (
          <Button onClick={() => window.location.href = '/dashboard'}>
            Go to Dashboard
          </Button>
        )}
      </div>
    </div>
  );
}
```

### Checklist Onboarding
```tsx
'use client';

import { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Check, Circle } from 'lucide-react';

interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  action: () => void;
}

export function OnboardingChecklist({ tasks }: { tasks: Task[] }) {
  const completedCount = tasks.filter(t => t.completed).length;
  const progress = (completedCount / tasks.length) * 100;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex justify-between">
          <span>Getting Started</span>
          <span className="text-sm font-normal text-muted-foreground">
            {completedCount}/{tasks.length} complete
          </span>
        </CardTitle>
        <Progress value={progress} className="mt-2" />
      </CardHeader>
      <CardContent>
        <ul className="space-y-3">
          {tasks.map((task) => (
            <li
              key={task.id}
              className={`flex items-start gap-3 p-3 rounded-lg cursor-pointer
                ${task.completed ? 'bg-muted' : 'hover:bg-muted/50'}`}
              onClick={task.action}
            >
              {task.completed ? (
                <Check className="w-5 h-5 text-green-500 mt-0.5" />
              ) : (
                <Circle className="w-5 h-5 text-muted-foreground mt-0.5" />
              )}
              <div>
                <p className={task.completed ? 'line-through text-muted-foreground' : 'font-medium'}>
                  {task.title}
                </p>
                <p className="text-sm text-muted-foreground">
                  {task.description}
                </p>
              </div>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}
```

### Tooltip Tour
```typescript
// Using react-joyride
import Joyride, { Step } from 'react-joyride';

const tourSteps: Step[] = [
  {
    target: '.sidebar-nav',
    content: 'Navigate between different sections here',
    placement: 'right',
  },
  {
    target: '.create-button',
    content: 'Click here to create your first project',
    placement: 'bottom',
  },
  {
    target: '.settings-icon',
    content: 'Customize your experience in settings',
    placement: 'left',
  },
];

export function AppWithTour() {
  const [runTour, setRunTour] = useState(true);

  return (
    <>
      <Joyride
        steps={tourSteps}
        run={runTour}
        continuous
        showProgress
        showSkipButton
        callback={(data) => {
          if (data.status === 'finished') {
            localStorage.setItem('tourCompleted', 'true');
          }
        }}
      />
      <App />
    </>
  );
}
```

## Onboarding Emails
```yaml
sequence:
  day_0:
    subject: "Welcome to [App] - Let's get started"
    content: Quick start guide + main CTA

  day_1:
    subject: "Did you know? [Key feature]"
    content: Feature highlight + tutorial link

  day_3:
    subject: "You're making progress!"
    content: Usage stats + next steps

  day_7:
    subject: "Questions? We're here to help"
    content: Support options + FAQ link
```

## Metrics to Track
```yaml
onboarding_metrics:
  - Completion rate per step
  - Time to complete onboarding
  - Drop-off points
  - Feature adoption rate
  - Time to first value action
```
