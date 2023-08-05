/*-----------------------------------------------------------------------------
| Copyright (c) 2014, Nucleic
|
| Distributed under the terms of the BSD 3-Clause License.
|
| The full license is in the file LICENSE, distributed with this software.
|----------------------------------------------------------------------------*/
#pragma once

#include <Python.h>

#define atomlist_cast( o ) ( reinterpret_cast<AtomList*>( o ) )


namespace atom
{

// POD struct - all member fields are considered private
struct TypedList
{
	PyListObject list;
	Member* validator;
	CAtomPointer* pointer;

	static PyTypeObject TypeObject;

	static bool Ready();

	static bool TypeCheck( PyObject* ob )
	{
		return PyObject_TypeCheck( ob, &TypeObject ) != 0;
	}
};

PyObject*
TypedList_New( Py_ssize_t size, CAtom* atom, Member* validator );

} // namespace atom
