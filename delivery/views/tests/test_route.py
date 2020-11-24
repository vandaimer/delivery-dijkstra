import mock

import pytest
from delivery.views import Route
from delivery.models import Route as RouteModel
from delivery.schemas import RouteSchema


from alchemy_mock.mocking import UnifiedAlchemyMagicMock, AlchemyMagicMock


class TestRoute:
    def setup_method(self):
        self.mock_data = {
            'map': 'map',
            'origin': 'origin',
            'destination': 'destination',
            'distance': 10
        }

    def test_validate_input(self):
        expected = False
        route_schema = RouteSchema(**self.mock_data)

        session = UnifiedAlchemyMagicMock(data=[
            (
                [mock.call.query(RouteModel.id),
                 mock.call.filter(
                     RouteModel.map == self.mock_data['map'],
                     RouteModel.origin == self.mock_data['origin'],
                     RouteModel.destination == self.mock_data['destination'])],
                [expected]
            ),
        ])

        route = Route(session)
        valid_input = route.validate_input(route_schema)

        assert valid_input == expected

    def test_validate_map(self):
        expected = 10
        session = UnifiedAlchemyMagicMock(data=[
            (
                [mock.call.query(RouteModel.id),
                 mock.call.filter(RouteModel.map == self.mock_data['map']),],
                [expected]
            ),
        ])

        route = Route(session)
        result = route.validate_map(self.mock_data['map'])

        session.query.return_value.filter.\
            assert_called_once_with(RouteModel.map == self.mock_data['map'])

    def test_validate_map_exception(self):
        expected = []
        session = UnifiedAlchemyMagicMock(data=[
            (
                [mock.call.query(RouteModel.id),
                 mock.call.filter(RouteModel.map == self.mock_data['map']),
                 ],
                expected,
            ),
        ])
        route = Route(session)

        with pytest.raises(ValueError, match='This map does not exists.'):
            route.validate_map(self.mock_data['map'])

    def test_validate_origin(self):
        expected = 10
        session = UnifiedAlchemyMagicMock(data=[
            (
                [mock.call.query(RouteModel.id),
                 mock.call.filter(RouteModel.map == self.mock_data['map'], RouteModel.origin == self.mock_data['origin']),],
                [expected],
            ),
        ])

        route = Route(session)
        route.validate_origin(self.mock_data['map'], self.mock_data['origin'])

        session.query.return_value.filter.\
            assert_called_once_with(RouteModel.map == self.mock_data['map'], RouteModel.origin == self.mock_data['origin'])

    def test_validate_origin_exception(self):
        expected = []
        session = UnifiedAlchemyMagicMock(data=[
            (
                [mock.call.query(RouteModel.id),
                 mock.call.filter(RouteModel.map == self.mock_data['map'], RouteModel.origin == self.mock_data['origin']),],
                expected,
            ),
        ])

        route = Route(session)

        with pytest.raises(ValueError, match='This origin on this map does not exists.'):
            route.validate_origin(self.mock_data['map'], self.mock_data['origin'])

    def test_validate_destination(self):
        expected = 10
        session = UnifiedAlchemyMagicMock(data=[
            (
                [mock.call.query(RouteModel.id),
                 mock.call.filter(RouteModel.map == self.mock_data['map'], RouteModel.destination == self.mock_data['destination']),],
                [expected],
            ),
        ])

        route = Route(session)
        route.validate_destination(self.mock_data['map'], self.mock_data['destination'])

        session.query.return_value.filter.\
            assert_called_once_with(RouteModel.map == self.mock_data['map'], RouteModel.destination == self.mock_data['destination'])

    def test_validate_destination_exception(self):
        expected = []
        session = UnifiedAlchemyMagicMock(data=[
            (
                [mock.call.query(RouteModel.id),
                 mock.call.filter(RouteModel.map == self.mock_data['map'], RouteModel.destination == self.mock_data['destination']),],
                expected,
            ),
        ])

        route = Route(session)

        with pytest.raises(ValueError, match='This destination on this map does not exists.'):
            route.validate_destination(self.mock_data['map'], self.mock_data['destination'])

    def test_calculate_cost(self):
        gas_price = 1
        truck_autonomy = 1
        distance = 0

        expected = 0

        result = Route.calculate_expenses(gas_price, truck_autonomy, distance)

        assert result == expected

    def test_validate_cheapest_input(self, mocker):
        session = AlchemyMagicMock()
        route = Route(session)

        spy_map = mocker.spy(route, 'validate_map')
        spy_origin = mocker.spy(route, 'validate_origin')
        spy_destination = mocker.spy(route, 'validate_destination')

        mocker.patch('delivery.views.route.Route.validate_map')
        mocker.patch('delivery.views.route.Route.validate_origin')
        mocker.patch('delivery.views.route.Route.validate_destination')

        route.validate_cheapest_input(self.mock_data)

        map = self.mock_data['map']

        spy_map.assert_called_once_with(map)
        spy_origin.assert_called_once_with(map, self.mock_data['origin'])
        spy_destination.assert_called_once_with(map, self.mock_data['destination'])
