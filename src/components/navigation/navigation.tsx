import * as React from 'react';
import navigationStyles from './navigation.module.css';
import { FC } from 'react';

interface INavigationProps {
  children: React.ReactNode
}

const Navigation: FC<INavigationProps> = ({ children }) => {
  return (
    <nav className={navigationStyles.nav}>
      {children}
    </nav>
  )
}

export default Navigation;