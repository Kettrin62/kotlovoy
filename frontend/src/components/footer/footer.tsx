import { Link } from 'react-router-dom';
import { dataFooter, pathNames } from '../../utils/data';
import Divider from '../divider/divider';
import Image from '../image/image';
import Navigation from '../navigation/navigation';
import Text from '../text/text';
import footerStyles from './footer.module.css';

function Footer() {
  return (
    <>
      <Divider />
      <footer className={footerStyles.footer}>
        <Text class={footerStyles.copy} text='&copy; Котловой62' />
        <div className={footerStyles.container}>
          <Navigation className={footerStyles.nav}>
            <Link className={footerStyles.link} to={pathNames.about}>
              <Text class={footerStyles.text} text='О нас' />
            </Link>
            <Link className={footerStyles.link} to={pathNames.contacts}>
              <Text class={footerStyles.text} text='Контакты' />
            </Link>
            <Link className={footerStyles.link} to={pathNames.feedback}>
              <Text class={footerStyles.text} text='Написать нам' />
            </Link>
          </Navigation>
        </div>
        <ul className={footerStyles.list}>
          {dataFooter.map((el, index) => (
            <li className={footerStyles.item} key={index}>
              <Image class={footerStyles.icon} src={el.image} alt={el.name}/>
              <Text class={footerStyles.text} text={el.text} />
            </li>
          ))}
        </ul>
      </footer>
    </>
  )
}

export default Footer;