<aside id="sidebar" class="sidebar">
    <ul class="sidebar-nav" id="sidebar-nav">

{{--        @if (Auth::user()->hasRole('admin'))--}}
        @if (Auth::user()->role === 'admin')
            <li class="nav-item">
                <a class="nav-link " href="{{ route('dashboard') }}">
                <i class="bi bi-grid"></i>
                <span>Dashboard</span>
                </a>
            </li><!-- End Dashboard Nav -->

            <li class="nav-item">
                <a class="nav-link collapsed" href="{{route('admin-employees')}}">
                    <i class="bi bi-people"></i>
                    <span>Wanted People</span>
                </a>
            </li><!-- End Profile Page Nav -->

            <li class="nav-item">
                <a class="nav-link collapsed" href="{{route('admin-attendances')}}">
                <i class="bi bi-asterisk"></i>
                <span>Detect Faces</span>
                </a>
            </li>

            <li class="nav-item">
                <a class="nav-link collapsed" href="">
                <i class="bi bi-card-list"></i>
                <span>Number Plates</span>
                </a>
            </li>

            <li class="nav-item">
                <a class="nav-link collapsed" href="">
                <i class="bi bi-person"></i>
                <span>Users</span>
                </a>
            </li>

            <li class="nav-item">
                <a class="nav-link collapsed" href="{{ route('criminals.index') }}">
                    <i class="bi bi-person"></i>
                    <span>Criminals</span>
                </a>
            </li>

            <li class="nav-item">
                <a class="nav-link collapsed" href="{{ route('vehicles.index') }}">
                    <i class="bi bi-list-check"></i>
                    <span>Vehicles</span>
                </a>
            </li>

        @else
            <li class="nav-item">
                <a class="nav-link collapsed" href="{{ route('citizens.index') }}">
                    <i class="bi bi-house"></i>
                    <span>Citizens</span>
                </a>
            </li>
            <li class="nav-item">
                <a class="nav-link collapsed" href="{{ route('vehicles.create') }}">
                    <i class="bi bi-list-check"></i>
                    <span>Vehicles</span>
                </a>
            </li>
        @endif
    </ul>
</aside>
