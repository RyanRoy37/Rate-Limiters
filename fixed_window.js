import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  scenarios: {
    rate_limit_demo: {
      executor: 'ramping-arrival-rate',
      startRate: 1,
      timeUnit: '1s',
      stages: [
        { target: 10, duration: '180s' },    
      //  { target: 10, duration: '30s' },   
       // { target: 2, duration: '30s' },   
      ],
      preAllocatedVUs: 20,
      maxVUs: 200,
    },
  },
};

export default function () {
  http.get('http://localhost:8000/request?algo=fixed_window');
  sleep(0.05);
}
