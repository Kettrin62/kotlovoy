import * as React from 'react';
import { useState, useEffect } from 'react';
import Navigation from '../navigation/navigation';
import hamburgerImg from '../../images/hamburger-menu.png';
import appHeaderStyles from './app-header.module.css';
import cn from 'classnames';
import navigation from '../../configs/navigation';
import LinkComponent from '../link/link-component';

function AppHeader() {

  const [ menuToggled, setMenuToggled ] = useState(false);
  const orders: any = [];

  return (
    <header>
      <div className={cn("App", {
        [appHeaderStyles.appMenuToggled]: menuToggled
      })}>
        <div
          className={appHeaderStyles.menuButton}
          onClick={_ => setMenuToggled(!menuToggled)}
        >
          <img src={hamburgerImg} />
        </div>
      <Navigation>
        <ul className={appHeaderStyles.nav}>
          {navigation.map(item => {
            // if (!loggedIn && item.auth) { return null }
            return <li className={cn(appHeaderStyles.nav__item, {
              [appHeaderStyles.nav__item_active]: false
            })} key={item.href}>
              <LinkComponent
                title={item.title}
                activeClassName={appHeaderStyles.nav__link_active}
                href={item.href}
                exact
                className={appHeaderStyles.nav__link}
              />
              {item.href === '/cart' && orders > 0 && <span className={appHeaderStyles['orders-count']}>{orders}</span>}
            </li>
          })}
        </ul>
      </Navigation>
      </div>
    </header>
  )
}

export default AppHeader;