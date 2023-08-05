/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
import {
  DASHBOARD_GRID_TYPE,
  DASHBOARD_HEADER_TYPE,
  DASHBOARD_ROOT_TYPE,
  TABS_TYPE,
  TAB_TYPE,
  CHART_TYPE,
  ROW_TYPE,
  COLUMN_TYPE,
  MARKDOWN_TYPE,
} from '../../../../src/dashboard/util/componentTypes';

import {
  DASHBOARD_ROOT_ID,
  DASHBOARD_HEADER_ID,
  DASHBOARD_GRID_ID,
} from '../../../../src/dashboard/util/constants';

import newComponentFactory from '../../../../src/dashboard/util/newComponentFactory';

import { sliceId as chartId } from './mockChartQueries';

export const sliceId = chartId;

export const dashboardLayout = {
  past: [],
  present: {
    [DASHBOARD_ROOT_ID]: {
      type: DASHBOARD_ROOT_TYPE,
      id: DASHBOARD_ROOT_ID,
      children: [DASHBOARD_GRID_ID],
    },

    [DASHBOARD_GRID_ID]: {
      type: DASHBOARD_GRID_TYPE,
      id: DASHBOARD_GRID_ID,
      children: ['ROW_ID'],
      meta: {},
    },

    [DASHBOARD_HEADER_ID]: {
      type: DASHBOARD_HEADER_TYPE,
      id: DASHBOARD_HEADER_ID,
      meta: {
        text: 'New dashboard',
      },
    },

    ROW_ID: {
      ...newComponentFactory(ROW_TYPE),
      id: 'ROW_ID',
      children: ['COLUMN_ID'],
    },

    COLUMN_ID: {
      ...newComponentFactory(COLUMN_TYPE),
      id: 'COLUMN_ID',
      children: ['CHART_ID'],
    },

    CHART_ID: {
      ...newComponentFactory(CHART_TYPE),
      id: 'CHART_ID',
      meta: {
        chartId,
        width: 3,
        height: 10,
        chartName: 'Mock chart name',
      },
    },

    MARKDOWN_ID: {
      ...newComponentFactory(MARKDOWN_TYPE),
      id: 'MARKDOWN_ID',
    },
  },
  future: [],
};

export const dashboardLayoutWithTabs = {
  past: [],
  present: {
    [DASHBOARD_ROOT_ID]: {
      type: DASHBOARD_ROOT_TYPE,
      id: DASHBOARD_ROOT_ID,
      children: ['TABS_ID'],
    },

    TABS_ID: {
      id: 'TABS_ID',
      type: TABS_TYPE,
      children: ['TAB_ID', 'TAB_ID2'],
    },

    TAB_ID: {
      id: 'TAB_ID',
      type: TAB_TYPE,
      children: ['ROW_ID'],
      meta: {
        text: 'tab1',
      },
    },

    TAB_ID2: {
      id: 'TAB_ID2',
      type: TAB_TYPE,
      children: [],
      meta: {
        text: 'tab2',
      },
    },

    CHART_ID: {
      ...newComponentFactory(CHART_TYPE),
      id: 'CHART_ID',
      meta: {
        chartId,
        width: 3,
        height: 10,
        chartName: 'Mock chart name',
      },
    },

    ROW_ID: {
      ...newComponentFactory(ROW_TYPE),
      id: 'ROW_ID',
      children: ['CHART_ID'],
    },

    [DASHBOARD_GRID_ID]: {
      type: DASHBOARD_GRID_TYPE,
      id: DASHBOARD_GRID_ID,
      children: [],
      meta: {},
    },

    [DASHBOARD_HEADER_ID]: {
      type: DASHBOARD_HEADER_TYPE,
      id: DASHBOARD_HEADER_ID,
      meta: {
        text: 'New dashboard',
      },
    },
  },
  future: [],
};
