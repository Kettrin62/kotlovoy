import * as React from 'react';
import { ReactNode, ErrorInfo } from "react";

interface IErrorBoundaryState {
  hasError: boolean
}
interface IErrorBoundaryProps {
  children?: ReactNode
}

export default class ErrorBoundary extends React.Component<IErrorBoundaryProps, IErrorBoundaryState> {
  constructor(props: IErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: boolean) {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.log("Возникла ошибка!", error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <section>
          <h1>Что-то пошло не так :(</h1>
          <p>
            В приложении произошла ошибка. Пожалуйста, перезагрузите страницу.
          </p>
        </section>
      );
    }
    return this.props.children;
  }
}