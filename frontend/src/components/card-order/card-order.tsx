import { FC, useCallback } from 'react';
import { 
  Link,
  useHistory,
  useLocation
} from 'react-router-dom';
import { TCardOrder } from '../../services/types/data';
import { showMessageDateTime } from '../../utils/functions';
import Divider from '../divider/divider';
import { priceFormat } from '../total-price/utils';
import cardorderStyles from './card-order.module.css';

interface ICardOrderProps {
  card: TCardOrder;
}

const CardOrder: FC<ICardOrderProps> = ({ card }) => {

  const { id, created, number, order_sum: totalPrice, status } = card;
  const date = showMessageDateTime(new Date(created), 'date');
  const history = useHistory();
  const pathname = useLocation().pathname

  const onClickOrder = useCallback(
    () => {
      if (pathname === '/profile/orders') history.replace({ pathname: `/profile/orders/${id}` });
      if (pathname === '/admin-panel/orders') history.replace({ pathname: `/admin-panel/orders/${id}` });
    },
    [history]
  );

  const statusName = status?.status ? status?.status : 'не указан'

  return (
    <li
      className={cardorderStyles.card}
      onClick={onClickOrder}
    >
      <h4 className={cardorderStyles.header}>
        {`№ ${number} от ${date}`}
      </h4>
      <p>
        {`Статус: ${statusName}`}
      </p>
      <p>
        {`Сумма: ${priceFormat(totalPrice)}`}
      </p>
    </li>
  )
}

export default CardOrder;