module model_mod

    type :: input_t
        integer :: nsteps
        integer :: save_restart_steps
    end type

contains

    function parse_command_line_arguments(file_path, beg_step, output_dir) result(res)
        implicit none
        character(len=*) :: file_path
        integer :: beg_step
        character(len=*) :: output_dir
        character(len=10) :: beg_step_str
        integer :: res

        res = 0

        file_path = 'model.nml'
        beg_step = 0
        output_dir = './'

        if (command_argument_count() >= 1) then
            call get_command_argument(1, file_path)
        endif
        print *, 'file_path = ', file_path

        if (command_argument_count() >= 2) then
            call get_command_argument(2, beg_step_str)
            read(beg_step_str, *) beg_step 
        endif
        print *, 'beg_step = ', beg_step

        if (command_argument_count() >= 3) then
            call get_command_argument(2, output_dir)
        endif
        print *, 'output_dir = ', output_dir

    end function parse_command_line_arguments

    function read_namelist(file_path, input_data) result(res)
        implicit none

        character(len=*) :: file_path
        type(input_t) :: input_data
        integer :: ier, fu, res
        integer :: nsteps, save_restart_steps
        namelist /input/ nsteps, save_restart_steps

        res = 0
        inquire(file=file_path, iostat=ier)
        if (ier /= 0) then
            res = 1
            return
        end if

        open(action='read', file=file_path, iostat=ier, newunit=fu)
        if (ier /= 0) then
            close(fu)
            res = 2
            return
        endif

        read(nml=input, iostat=ier, unit=fu)
        if (ier /= 0) then
            res = 3
            return
        endif

        close(fu)

        input_data%nsteps = nsteps
        input_data%save_restart_steps = save_restart_steps
    end function read_namelist

    subroutine write_output(i, output_dir)
            implicit none
            integer :: i, fu, ier
            character(len=*) :: output_dir
            character(len=256) :: file_name
            character(len=10) :: index_str

            write(index_str, '(I0)') i
            
            file_name = output_dir // 'model_output_' // trim(index_str) // '.txt'
            print *, 'writing ', file_name
            open(action='write', file=file_name, iostat=ier, newunit=fu)
            close(fu)

    end subroutine write_output

end module model_mod

program model

    use model_mod

    implicit none
    integer :: ier
    character(len=256) :: file_path
    character(len=256) :: output_dir
    integer :: i, beg_step
    type(input_t) :: input_data
    real :: r

    ier = parse_command_line_arguments(file_path, beg_step, output_dir)
    if (ier /= 0) error stop 'ERROR parsing command line arguments'

    ! read namelist
    ier = read_namelist(file_path, input_data)
    if (ier /= 0) error stop 'ERROR reading the namelist'

    ! loop
    do i = beg_step + 1, input_data%nsteps

        call sleep(1) ! simulate number crunching

        if ( modulo(i - beg_step + 1, 8) == 0 ) then
            ! fail every N times
            stop 1
        endif

        if ( modulo(i, input_data%save_restart_steps) == 0 ) then
            call write_output(i, output_dir)
        end if
    enddo

    stop 0 ! success

end program model